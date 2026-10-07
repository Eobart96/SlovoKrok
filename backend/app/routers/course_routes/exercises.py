from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import CourseExercise, CourseExerciseAttempt
from app.routers.course_routes.common import commit_course_change, invoke_tutor
from app.schemas.course import (
    CourseExerciseAnswerRequest,
    CourseExerciseAttemptResponse,
    CourseExerciseGenerateRequest,
    CourseExerciseResponse,
)
from app.tutor import (
    AIResponseError,
    TutorProvider,
    assess_exercise_offline,
    build_generated_exercise_context,
    build_tutor_context,
    decode_exercise_snapshot,
    encode_exercise_snapshot,
    parse_generated_exercise,
    parse_tutor_assessment,
    requested_exercise_interaction,
)


router = APIRouter()


def _exercise_response(db: Session, exercise: CourseExercise) -> CourseExerciseResponse:
    attempt = db.scalar(select(CourseExerciseAttempt).where(CourseExerciseAttempt.exercise_id == exercise.id).order_by(CourseExerciseAttempt.id.desc()))
    _, interaction = decode_exercise_snapshot(exercise.theory_snapshot)
    pair_prompts = [pair.prompt for pair in interaction.pairs]
    pair_options = [pair.answer for pair in interaction.pairs]
    if len(pair_options) > 1:
        shift = exercise.id % (len(pair_options) - 1) + 1
        pair_options = pair_options[shift:] + pair_options[:shift]
    return CourseExerciseResponse(
        id=exercise.id,
        lesson_slug=exercise.lesson_slug,
        lesson_title=exercise.lesson_title,
        question=exercise.question,
        instruction=exercise.instruction,
        interaction_type=interaction.interaction_type,
        options=interaction.options,
        tokens=interaction.tokens,
        pair_prompts=pair_prompts,
        pair_options=pair_options,
        created_at=exercise.created_at,
        latest_attempt=CourseExerciseAttemptResponse.model_validate(attempt, from_attributes=True) if attempt else None,
    )


@router.get("/exercises", response_model=list[CourseExerciseResponse])
def list_exercises(lesson_slug: str | None = None, db: Session = Depends(get_db)) -> list[CourseExerciseResponse]:
    query = select(CourseExercise).order_by(CourseExercise.id.desc())
    if lesson_slug:
        query = query.where(CourseExercise.lesson_slug == lesson_slug)
    return [_exercise_response(db, item) for item in db.scalars(query).all()]


@router.post("/exercises", response_model=CourseExerciseResponse)
def generate_exercise(request: CourseExerciseGenerateRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseExerciseResponse:
    def generate():
        result = parse_generated_exercise(provider.respond(build_generated_exercise_context(lesson_title=request.lesson_title, theory=request.theory)))
        requested_interaction = requested_exercise_interaction(request.theory)
        if requested_interaction and result.interaction_type != requested_interaction:
            raise AIResponseError(f"Generator returned {result.interaction_type} instead of {requested_interaction}")
        return result

    generated = invoke_tutor(generate)
    exercise = CourseExercise(lesson_slug=request.lesson_slug, lesson_title=request.lesson_title, question=generated.question, instruction=generated.instruction, theory_snapshot=encode_exercise_snapshot(request.theory, generated))
    db.add(exercise)
    commit_course_change(db)
    db.refresh(exercise)
    return _exercise_response(db, exercise)


@router.post("/exercises/{exercise_id}/answer", response_model=CourseExerciseAttemptResponse)
def answer_exercise(exercise_id: int, request: CourseExerciseAnswerRequest, db: Session = Depends(get_db), provider: TutorProvider = Depends(get_tutor_provider)) -> CourseExerciseAttemptResponse:
    exercise = db.get(CourseExercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Module 1 exercise not found")
    theory, interaction = decode_exercise_snapshot(exercise.theory_snapshot)
    has_reference = bool(interaction.pairs) if interaction.interaction_type == "match" else bool(interaction.accepted_answers)
    if has_reference or request.assessment_mode == "offline":
        try:
            assessment = assess_exercise_offline(interaction=interaction, answer=request.answer)
        except ValueError as error:
            raise HTTPException(status_code=409, detail="Для этого старого упражнения нет сохранённого эталона. Переключитесь в онлайн-режим.") from error
    else:
        interaction_details = interaction.model_dump_json()
        prompt = f"""Проверь ответ на отдельное упражнение словацкого A1.\nТема: {exercise.lesson_title}\nТеория: {theory}\nЗадание: {exercise.question}\nИнструкция: {exercise.instruction}\nСкрытая структура интерактива с сохранённым эталоном: {interaction_details}\nОтвет ученика: {request.answer}\nСначала сравни с сохранённым эталоном, но допускай равноценную формулировку, если она правильна по теории.\nВерни только JSON: {{"is_correct":false,"score":0,"corrected_answer":"","explanation":"объяснение по-русски","next_exercise":"следующий короткий шаг","mistake_category":null,"new_words":[]}}"""
        assessment = invoke_tutor(lambda: parse_tutor_assessment(provider.respond(build_tutor_context(get_settings(), prompt))))
    attempt = CourseExerciseAttempt(exercise_id=exercise.id, answer=request.answer, is_correct=assessment.is_correct, score=assessment.score, corrected_answer=assessment.corrected_answer, explanation=assessment.explanation, next_exercise=assessment.next_exercise)
    db.add(attempt)
    commit_course_change(db)
    db.refresh(attempt)
    return CourseExerciseAttemptResponse.model_validate(attempt, from_attributes=True)


class _DeleteAllExercisesRequest(BaseModel):
    confirmation: Literal["delete-all-exercises"]


@router.delete("/exercises")
def delete_all_exercises(request: _DeleteAllExercisesRequest, db: Session = Depends(get_db)) -> dict[str, int | bool]:
    exercise_count = db.query(CourseExercise).count()
    attempt_count = db.query(CourseExerciseAttempt).count()
    db.query(CourseExerciseAttempt).delete(synchronize_session=False)
    db.query(CourseExercise).delete(synchronize_session=False)
    commit_course_change(db)
    return {"deleted": True, "exercises_deleted": exercise_count, "attempts_deleted": attempt_count}


@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    exercise = db.get(CourseExercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Module 1 exercise not found")
    db.query(CourseExerciseAttempt).filter(CourseExerciseAttempt.exercise_id == exercise.id).delete(synchronize_session=False)
    db.delete(exercise)
    commit_course_change(db)
    return {"deleted": True}
