from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import CourseHomework, CourseHomeworkAttempt
from app.routers.course_routes.common import invoke_tutor
from app.schemas.course import (
    CourseHomeworkAttemptResponse,
    CourseHomeworkGenerateRequest,
    CourseHomeworkResponse,
    CourseHomeworkSubmitRequest,
)
from app.tutor import TutorProvider, build_tutor_context, parse_homework_generation, parse_tutor_assessment


router = APIRouter()


def _homework_response(db: Session, homework: CourseHomework) -> CourseHomeworkResponse:
    attempt = db.scalar(select(CourseHomeworkAttempt).where(CourseHomeworkAttempt.homework_id == homework.id).order_by(CourseHomeworkAttempt.id.desc()))
    return CourseHomeworkResponse(
        id=homework.id, lesson_slug=homework.lesson_slug, lesson_title=homework.lesson_title,
        title=homework.title, description=homework.description, focus_category=homework.focus_category,
        created_at=homework.created_at,
        latest_attempt=CourseHomeworkAttemptResponse.model_validate(attempt, from_attributes=True) if attempt else None,
    )


@router.get("/homework", response_model=list[CourseHomeworkResponse])
def list_course_homework(db: Session = Depends(get_db)) -> list[CourseHomeworkResponse]:
    return [_homework_response(db, item) for item in db.scalars(select(CourseHomework).order_by(CourseHomework.id.desc())).all()]


@router.post("/homework", response_model=CourseHomeworkResponse)
def generate_course_homework(request: CourseHomeworkGenerateRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseHomeworkResponse:
    mistakes = "\n".join(f"- {item}" for item in request.known_mistakes) or "Нет сохранённых ошибок."
    prompt = f"""Создай одно небольшое домашнее задание для начинающего изучать словацкий A1.
Тема: {request.lesson_title}
Теория (не выходи за её пределы):
{request.theory}
Известные ошибки ученика:
{mistakes}
Задание должно требовать короткий самостоятельный ответ на словацком и занимать 5–10 минут.
Верни только JSON: {{"title":"короткое название","description":"понятная инструкция по-русски","focus_category":"навык или правило"}}"""
    generated = invoke_tutor(lambda: parse_homework_generation(provider.respond(build_tutor_context(get_settings(), prompt))))
    homework = CourseHomework(lesson_slug=request.lesson_slug, lesson_title=request.lesson_title, title=generated.title, description=generated.description, focus_category=generated.focus_category, theory_snapshot=request.theory)
    db.add(homework)
    db.commit()
    db.refresh(homework)
    return _homework_response(db, homework)


@router.post("/homework/{homework_id}/submit", response_model=CourseHomeworkAttemptResponse)
def submit_course_homework(homework_id: int, request: CourseHomeworkSubmitRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseHomeworkAttemptResponse:
    homework = db.get(CourseHomework, homework_id)
    if homework is None:
        raise HTTPException(status_code=404, detail="Module 1 homework not found")
    prompt = f"""Проверь домашнее задание начинающего изучать словацкий A1.
Тема: {homework.lesson_title}
Теория (единственная граница проверки): {homework.theory_snapshot}
Задание: {homework.description}
Ответ ученика: {request.answer}
Верни только JSON: {{"is_correct":false,"score":0,"corrected_answer":"","explanation":"простое объяснение по-русски","next_exercise":"что повторить","mistake_category":null,"new_words":[]}}"""
    assessment = invoke_tutor(lambda: parse_tutor_assessment(provider.respond(build_tutor_context(get_settings(), prompt))))
    attempt = CourseHomeworkAttempt(homework_id=homework.id, answer=request.answer, is_correct=assessment.is_correct, score=assessment.score, corrected_answer=assessment.corrected_answer, explanation=assessment.explanation, next_exercise=assessment.next_exercise)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return CourseHomeworkAttemptResponse.model_validate(attempt, from_attributes=True)


@router.delete("/homework/{homework_id}")
def delete_course_homework(homework_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    homework = db.get(CourseHomework, homework_id)
    if homework is None:
        raise HTTPException(status_code=404, detail="Module 1 homework not found")
    db.query(CourseHomeworkAttempt).filter(CourseHomeworkAttempt.homework_id == homework.id).delete(synchronize_session=False)
    db.delete(homework)
    db.commit()
    return {"deleted": True}
