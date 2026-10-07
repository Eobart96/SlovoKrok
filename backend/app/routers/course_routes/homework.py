import re
from dataclasses import replace

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import CourseHomework, CourseHomeworkAttempt
from app.routers.course_routes.common import commit_course_change, invoke_tutor
from app.schemas.course import (
    CourseHomeworkAttemptResponse,
    CourseHomeworkGenerateRequest,
    CourseHomeworkResponse,
    CourseHomeworkSubmitRequest,
)
from app.tutor import TutorAssessment, TutorProvider, build_tutor_context, parse_homework_generation, parse_tutor_assessment
from app.tutor_core.offline import assess_open_answer_offline


router = APIRouter()


SEQUENCE_SEPARATOR_RE = re.compile(r"\s+(?:-|–|—|−|→)\s+")


def normalize_homework_sequence_separators(answer: str) -> str:
    """Treat keyboard-friendly dashes as arrows when they separate chain items."""
    return SEQUENCE_SEPARATOR_RE.sub(" → ", answer.strip())


def _homework_response(db: Session, homework: CourseHomework) -> CourseHomeworkResponse:
    attempt = db.scalar(select(CourseHomeworkAttempt).where(CourseHomeworkAttempt.homework_id == homework.id).order_by(CourseHomeworkAttempt.id.desc()))
    return CourseHomeworkResponse(
        id=homework.id, lesson_slug=homework.lesson_slug, lesson_title=homework.lesson_title,
        title=homework.title, description=homework.description, focus_category=homework.focus_category,
        created_at=homework.created_at, offline_ready=bool(homework.reference_answer),
        latest_attempt=CourseHomeworkAttemptResponse.model_validate(attempt, from_attributes=True) if attempt else None,
    )


@router.get("/homework", response_model=list[CourseHomeworkResponse])
def list_course_homework(db: Session = Depends(get_db)) -> list[CourseHomeworkResponse]:
    return [_homework_response(db, item) for item in db.scalars(select(CourseHomework).order_by(CourseHomework.id.desc())).all()]


@router.post("/homework", response_model=CourseHomeworkResponse)
def generate_course_homework(request: CourseHomeworkGenerateRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseHomeworkResponse:
    mistakes = "\n".join(f"- {item}" for item in request.known_mistakes) or "Нет сохранённых ошибок."
    variation = (
        f"Это вариант {request.batch_index} из {request.batch_total} в одном наборе. Сделай его заметно отличающимся от других вариантов набора."
        if request.batch_total > 1
        else ""
    )
    prompt = f"""Создай одно небольшое домашнее задание для начинающего изучать словацкий A1.
Тема: {request.lesson_title}
Теория (не выходи за её пределы):
{request.theory}
Известные ошибки ученика:
{mistakes}
{variation}
Задание должно требовать короткий самостоятельный ответ на словацком и занимать 5–10 минут.
Теория ограничивает грамматику задания, но не словарный запас: слова ученик изучает в разных источниках.
Не называй слова «изученными» или «неизученными» и не требуй использовать слова только из выбранной темы.
Если в ответе нужна цепочка, разреши соединять элементы стрелкой, дефисом или тире и явно укажи это в условии.
Верни только JSON: {{"title":"короткое название","description":"понятная инструкция по-русски","focus_category":"навык или правило","reference_answer":"один полный образец правильного ответа по-словацки для офлайн-проверки"}}"""
    generated = invoke_tutor(lambda: parse_homework_generation(provider.respond(build_tutor_context(get_settings(), prompt))))
    homework = CourseHomework(lesson_slug=request.lesson_slug, lesson_title=request.lesson_title, title=generated.title, description=generated.description, focus_category=generated.focus_category, theory_snapshot=request.theory, reference_answer=generated.reference_answer)
    db.add(homework)
    commit_course_change(db)
    db.refresh(homework)
    return _homework_response(db, homework)


@router.post("/homework/{homework_id}/submit", response_model=CourseHomeworkAttemptResponse)
def submit_course_homework(homework_id: int, request: CourseHomeworkSubmitRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseHomeworkAttemptResponse:
    homework = db.get(CourseHomework, homework_id)
    if homework is None:
        raise HTTPException(status_code=404, detail="Module 1 homework not found")
    if request.assessment_mode == "offline":
        if not homework.reference_answer:
            raise HTTPException(status_code=409, detail="Для этого старого задания нет офлайн-эталона. Проверьте его онлайн.")
        offline = assess_open_answer_offline(request.answer, homework.reference_answer)
        assessment = TutorAssessment(
            is_correct=offline.is_correct,
            score=offline.score,
            corrected_answer=homework.reference_answer,
            explanation=(
                "Ответ совпадает с ключевыми элементами сохранённого эталона."
                if offline.is_correct
                else "В ответе не хватает ключевых элементов сохранённого эталона."
            ),
            next_exercise="Сравните свой ответ с эталоном и перепишите отличающиеся фразы.",
            mistake_category=None if offline.is_correct else homework.focus_category,
            new_words=[],
        )
    else:
        answer_for_assessment = normalize_homework_sequence_separators(request.answer)
        prompt = f"""Проверь домашнее задание начинающего изучать словацкий A1.
Тема: {homework.lesson_title}
Теория (единственная граница проверки): {homework.theory_snapshot}
Задание: {homework.description}
Ответ ученика: {answer_for_assessment}
Словарный запас ученика приходит из разных источников и не ограничен теорией этой темы или отмеченным прогрессом курса.
Не снижай оценку, не называй слово неизученным и не требуй заменить его только потому, что его нет в теории или списке темы.
Если слово написано правильно и выполняет условие задания, принимай его независимо от источника. Ошибки в языке и невыполненные пункты задания по-прежнему исправляй честно.
В цепочках считай разделители →, -, – и — равнозначными. Не снижай оценку за дефис или тире вместо стрелки: на обычной клавиатуре стрелки может не быть.
Верни только JSON с полями is_correct (boolean), score (целое число от 0 до 100), corrected_answer, explanation, next_exercise, mistake_category и new_words.
Определи оценку по ответу ученика; правильный ответ получает 100. corrected_answer всегда содержит полный правильный ответ по-словацки, даже если ответ ученика уже правильный. explanation и next_exercise — непустые строки по-русски. mistake_category — строка или null; new_words — массив объектов word, translation, example или пустой массив."""
        schema = TutorAssessment.model_json_schema()
        # Structured output requires all object properties, including nullable ones.
        schema["required"] = list(schema["properties"])
        for definition in schema.get("$defs", {}).values():
            if "properties" in definition:
                definition["required"] = list(definition["properties"])
        context = replace(build_tutor_context(get_settings(), prompt), response_schema=schema)
        assessment = invoke_tutor(lambda: parse_tutor_assessment(provider.respond(context)))
    attempt = CourseHomeworkAttempt(homework_id=homework.id, answer=request.answer, is_correct=assessment.is_correct, score=assessment.score, corrected_answer=assessment.corrected_answer, explanation=assessment.explanation, next_exercise=assessment.next_exercise)
    db.add(attempt)
    commit_course_change(db)
    db.refresh(attempt)
    return CourseHomeworkAttemptResponse.model_validate(attempt, from_attributes=True)


@router.delete("/homework/{homework_id}")
def delete_course_homework(homework_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    homework = db.get(CourseHomework, homework_id)
    if homework is None:
        raise HTTPException(status_code=404, detail="Module 1 homework not found")
    db.query(CourseHomeworkAttempt).filter(CourseHomeworkAttempt.homework_id == homework.id).delete(synchronize_session=False)
    db.delete(homework)
    commit_course_change(db)
    return {"deleted": True}
