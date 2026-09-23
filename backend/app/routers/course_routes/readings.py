from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import CourseReading, CourseReadingAttempt
from app.routers.course_routes.common import invoke_tutor
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


router = APIRouter()


class _GeneratedReading(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=8_000)
    instruction: str = Field(min_length=1, max_length=1_000)


def _reading_response(db: Session, reading: CourseReading) -> CourseReadingResponse:
    attempt = db.scalar(select(CourseReadingAttempt).where(CourseReadingAttempt.reading_id == reading.id).order_by(CourseReadingAttempt.id.desc()))
    return CourseReadingResponse(id=reading.id, lesson_slug=reading.lesson_slug, lesson_title=reading.lesson_title, title=reading.title, text=reading.text, instruction=reading.instruction, created_at=reading.created_at, latest_attempt=CourseReadingAttemptResponse.model_validate(attempt, from_attributes=True) if attempt else None)


@router.get("/readings", response_model=list[CourseReadingResponse])
def list_readings(db: Session = Depends(get_db)) -> list[CourseReadingResponse]:
    return [_reading_response(db, item) for item in db.scalars(select(CourseReading).order_by(CourseReading.id.desc())).all()]


@router.post("/readings", response_model=CourseReadingResponse)
def generate_reading(request: CourseReadingGenerateRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseReadingResponse:
    generated = invoke_tutor(lambda: parse_ai_json(
        provider.respond(build_reading_generation_context(lesson_title=request.lesson_title, theory=request.theory, completed_theory=request.completed_theory)),
        _GeneratedReading,
    ))
    reading = CourseReading(lesson_slug=request.lesson_slug, lesson_title=request.lesson_title, title=generated.title, text=generated.text, instruction=generated.instruction)
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return _reading_response(db, reading)


@router.post("/readings/{reading_id}/check", response_model=CourseReadingAttemptResponse)
def check_reading(reading_id: int, request: CourseReadingCheckRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseReadingAttemptResponse:
    reading = db.get(CourseReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=404, detail="Module 1 reading not found")
    checked = invoke_tutor(lambda: parse_ai_json(
        provider.respond(build_reading_check_context(text=reading.text, retelling=request.retelling)),
        CourseReadingCheckResult,
    ))
    attempt = CourseReadingAttempt(reading_id=reading.id, retelling=request.retelling, score=checked.score, feedback=checked.feedback, corrected_retelling=checked.corrected_retelling)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return CourseReadingAttemptResponse.model_validate(attempt, from_attributes=True)


@router.delete("/readings/{reading_id}")
def delete_reading(reading_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    reading = db.get(CourseReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=404, detail="Module 1 reading not found")
    db.query(CourseReadingAttempt).filter(CourseReadingAttempt.reading_id == reading.id).delete(synchronize_session=False)
    db.delete(reading)
    db.commit()
    return {"deleted": True}
