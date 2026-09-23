import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_tutor_provider
from app.models import TranslationHistoryEntry, TranslationHistoryQuestion
from app.routers.tutor_routes.common import invoke_tutor
from app.schemas.tutor import (
    TutorTranslationHistoryClearRequest,
    TutorTranslationHistoryQuestionResponse,
    TutorTranslationHistoryResponse,
    TutorTranslationQuestionRequest,
    TutorTranslationQuestionResponse,
    TutorTranslationRequest,
    TutorTranslationResponse,
)
from app.tutor import (
    TutorProvider,
    build_translation_context,
    build_translation_question_context,
    parse_tutor_translation,
    parse_tutor_translation_question,
)


router = APIRouter()


@router.post("/api/v1/tutor/translate", response_model=TutorTranslationResponse)
def translate(
    request: TutorTranslationRequest,
    provider: TutorProvider = Depends(get_tutor_provider),
    db: Session = Depends(get_db),
) -> TutorTranslationResponse:
    result = invoke_tutor(lambda: parse_tutor_translation(
        provider.respond(build_translation_context(text=request.text, direction=request.direction))
    ))
    provider_name = get_settings().tutor_provider
    history = TranslationHistoryEntry(
        direction=request.direction,
        source_text=request.text,
        translation=result.translation,
        alternatives_json=json.dumps(result.alternatives, ensure_ascii=False),
        note=result.note,
        provider=provider_name,
    )
    try:
        db.add(history)
        db.flush()
        history_id = history.id
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=503, detail="Не удалось сохранить перевод в локальной истории") from error
    return TutorTranslationResponse(history_id=history_id, provider=provider_name, **result.model_dump())


@router.post("/api/v1/tutor/translate-question", response_model=TutorTranslationQuestionResponse)
def ask_translation_question(
    request: TutorTranslationQuestionRequest,
    provider: TutorProvider = Depends(get_tutor_provider),
    db: Session = Depends(get_db),
) -> TutorTranslationQuestionResponse:
    history = db.get(TranslationHistoryEntry, request.history_id) if request.history_id else None
    if request.history_id and history is None:
        raise HTTPException(status_code=404, detail="Перевод в истории не найден")
    source_text = history.source_text if history else request.source_text
    translation = history.translation if history else request.translation
    direction = history.direction if history else request.direction
    result = invoke_tutor(lambda: parse_tutor_translation_question(
        provider.respond(build_translation_question_context(
            source_text=source_text,
            translation=translation,
            direction=direction,
            question=request.question,
        ))
    ))
    provider_name = get_settings().tutor_provider
    try:
        if history is None:
            history = TranslationHistoryEntry(
                direction=direction,
                source_text=source_text,
                translation=translation,
                alternatives_json="[]",
                provider=provider_name,
            )
            db.add(history)
            db.flush()
        db.add(TranslationHistoryQuestion(
            translation_id=history.id,
            question=request.question,
            answer=result.answer,
            provider=provider_name,
        ))
        history_id = history.id
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=503, detail="Не удалось сохранить вопрос в локальной истории") from error
    return TutorTranslationQuestionResponse(history_id=history_id, provider=provider_name, answer=result.answer)


def _translation_history_responses(
    db: Session,
    entries: list[TranslationHistoryEntry],
) -> list[TutorTranslationHistoryResponse]:
    if not entries:
        return []
    questions_by_translation: dict[int, list[TranslationHistoryQuestion]] = {entry.id: [] for entry in entries}
    questions = db.scalars(
        select(TranslationHistoryQuestion)
        .where(TranslationHistoryQuestion.translation_id.in_(questions_by_translation))
        .order_by(TranslationHistoryQuestion.id)
    ).all()
    for question in questions:
        questions_by_translation[question.translation_id].append(question)

    responses: list[TutorTranslationHistoryResponse] = []
    for entry in entries:
        try:
            raw_alternatives = json.loads(entry.alternatives_json)
        except (json.JSONDecodeError, TypeError):
            raw_alternatives = []
        alternatives = (
            [item for item in raw_alternatives if isinstance(item, str) and 0 < len(item) <= 4_000][:2]
            if isinstance(raw_alternatives, list)
            else []
        )
        responses.append(TutorTranslationHistoryResponse(
            id=entry.id,
            direction=entry.direction,
            source_text=entry.source_text,
            translation=entry.translation,
            alternatives=alternatives,
            note=entry.note,
            provider=entry.provider,
            created_at=entry.created_at,
            questions=[
                TutorTranslationHistoryQuestionResponse.model_validate(item, from_attributes=True)
                for item in questions_by_translation[entry.id]
            ],
        ))
    return responses


@router.get("/api/v1/tutor/translation-history", response_model=list[TutorTranslationHistoryResponse])
def get_translation_history(
    limit: int = Query(default=50, ge=1, le=200),
    before_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
) -> list[TutorTranslationHistoryResponse]:
    statement = select(TranslationHistoryEntry)
    if before_id is not None:
        statement = statement.where(TranslationHistoryEntry.id < before_id)
    entries = list(db.scalars(statement.order_by(TranslationHistoryEntry.id.desc()).limit(limit)).all())
    return _translation_history_responses(db, entries)


@router.delete("/api/v1/tutor/translation-history/{history_id}")
def delete_translation_history(history_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    entry = db.get(TranslationHistoryEntry, history_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Перевод в истории не найден")
    db.query(TranslationHistoryQuestion).filter(
        TranslationHistoryQuestion.translation_id == entry.id
    ).delete(synchronize_session=False)
    db.delete(entry)
    db.commit()
    return {"deleted": True}


@router.delete("/api/v1/tutor/translation-history")
def clear_translation_history(
    request: TutorTranslationHistoryClearRequest,
    db: Session = Depends(get_db),
) -> dict[str, int | bool]:
    translation_count = db.query(TranslationHistoryEntry).count()
    question_count = db.query(TranslationHistoryQuestion).count()
    db.query(TranslationHistoryQuestion).delete(synchronize_session=False)
    db.query(TranslationHistoryEntry).delete(synchronize_session=False)
    db.commit()
    return {"deleted": True, "translations_deleted": translation_count, "questions_deleted": question_count}
