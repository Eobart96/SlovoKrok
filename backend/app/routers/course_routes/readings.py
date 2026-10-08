from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import CourseReading, CourseReadingAttempt
from app.routers.course_routes.common import commit_course_change, invoke_tutor, course_level_for_slug
from app.schemas.course import (
    CourseReadingAttemptResponse,
    CourseReadingCheckRequest,
    CourseReadingCheckResult,
    CourseReadingGenerateRequest,
    CourseReadingResponse,
)
from app.tutor import (
    TutorProvider,
    build_reading_check_context,
    build_reading_generation_context,
    parse_ai_json,
)
from app.tutor_core.offline import assess_open_answer_offline


router = APIRouter()


class _GeneratedReading(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=8_000)
    instruction: str = Field(min_length=1, max_length=1_000)
    reference_answer: str = Field(min_length=1, max_length=4_000)


def _reading_response(db: Session, reading: CourseReading) -> CourseReadingResponse:
    attempt = db.scalar(select(CourseReadingAttempt).where(CourseReadingAttempt.reading_id == reading.id).order_by(CourseReadingAttempt.id.desc()))
    return CourseReadingResponse(id=reading.id, lesson_slug=reading.lesson_slug, lesson_title=reading.lesson_title, title=reading.title, text=reading.text, instruction=reading.instruction, created_at=reading.created_at, offline_ready=bool(reading.reference_answer), latest_attempt=CourseReadingAttemptResponse.model_validate(attempt, from_attributes=True) if attempt else None)


@router.get("/readings", response_model=list[CourseReadingResponse])
def list_readings(db: Session = Depends(get_db)) -> list[CourseReadingResponse]:
    return [_reading_response(db, item) for item in db.scalars(select(CourseReading).order_by(CourseReading.id.desc())).all()]


@router.post("/readings", response_model=CourseReadingResponse)
def generate_reading(request: CourseReadingGenerateRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseReadingResponse:
    generated = invoke_tutor(lambda: parse_ai_json(
        provider.respond(build_reading_generation_context(
            lesson_title=request.lesson_title,
            theory=request.theory,
            completed_theory=request.completed_theory,
            batch_index=request.batch_index,
            batch_total=request.batch_total,
            level=course_level_for_slug(request.lesson_slug),
        )),
        _GeneratedReading,
    ))
    reading = CourseReading(lesson_slug=request.lesson_slug, lesson_title=request.lesson_title, title=generated.title, text=generated.text, instruction=generated.instruction, reference_answer=generated.reference_answer)
    db.add(reading)
    commit_course_change(db)
    db.refresh(reading)
    return _reading_response(db, reading)


@router.post("/readings/{reading_id}/check", response_model=CourseReadingAttemptResponse)
def check_reading(reading_id: int, request: CourseReadingCheckRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseReadingAttemptResponse:
    reading = db.get(CourseReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=404, detail="Module 1 reading not found")
    if request.assessment_mode == "offline":
        if not reading.reference_answer:
            raise HTTPException(status_code=409, detail="Для этого старого текста нет офлайн-эталона. Проверьте его онлайн.")
        offline = assess_open_answer_offline(request.retelling, reading.reference_answer)
        checked = CourseReadingCheckResult(
            score=offline.score,
            feedback=(
                "Основной смысл передан по сохранённому эталону."
                if offline.is_correct
                else "В пересказе не хватает ключевых событий из сохранённого эталона."
            ),
            corrected_retelling=reading.reference_answer,
        )
    else:
        checked = invoke_tutor(lambda: parse_ai_json(
            provider.respond(build_reading_check_context(text=reading.text, retelling=request.retelling)),
            CourseReadingCheckResult,
        ))
    attempt = CourseReadingAttempt(reading_id=reading.id, retelling=request.retelling, score=checked.score, feedback=checked.feedback, corrected_retelling=checked.corrected_retelling)
    db.add(attempt)
    commit_course_change(db)
    db.refresh(attempt)
    return CourseReadingAttemptResponse.model_validate(attempt, from_attributes=True)


@router.delete("/readings/{reading_id}")
def delete_reading(reading_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    reading = db.get(CourseReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=404, detail="Module 1 reading not found")
    db.query(CourseReadingAttempt).filter(CourseReadingAttempt.reading_id == reading.id).delete(synchronize_session=False)
    db.delete(reading)
    commit_course_change(db)
    return {"deleted": True}
