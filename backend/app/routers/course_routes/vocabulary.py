from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CourseVocabularyItem
from app.schemas.course import CourseVocabularyResponse, CourseVocabularySyncRequest


router = APIRouter()


def _vocabulary_response(item: CourseVocabularyItem) -> CourseVocabularyResponse:
    now = datetime.now(timezone.utc)
    due = item.next_review_at is None or item.next_review_at.replace(tzinfo=timezone.utc) <= now
    return CourseVocabularyResponse.model_validate({**item.__dict__, "is_due": due})


@router.put("/vocabulary/sync", response_model=list[CourseVocabularyResponse])
def sync_vocabulary(request: CourseVocabularySyncRequest, db: Session = Depends(get_db)) -> list[CourseVocabularyResponse]:
    if request.items:
        statement = sqlite_insert(CourseVocabularyItem).values(
            [incoming.model_dump() for incoming in request.items]
        )
        statement = statement.on_conflict_do_update(
            index_elements=[CourseVocabularyItem.lesson_slug, CourseVocabularyItem.word],
            set_={
                "lesson_title": statement.excluded.lesson_title,
                "translation": statement.excluded.translation,
                "example": statement.excluded.example,
            },
        )
        db.execute(statement)
    db.commit()
    return [_vocabulary_response(item) for item in db.scalars(select(CourseVocabularyItem).order_by(CourseVocabularyItem.lesson_slug, CourseVocabularyItem.id)).all()]


@router.get("/vocabulary", response_model=list[CourseVocabularyResponse])
def list_vocabulary(db: Session = Depends(get_db)) -> list[CourseVocabularyResponse]:
    return [_vocabulary_response(item) for item in db.scalars(select(CourseVocabularyItem).order_by(CourseVocabularyItem.lesson_slug, CourseVocabularyItem.id)).all()]


@router.post("/vocabulary/{item_id}/review", response_model=CourseVocabularyResponse)
def review_vocabulary(item_id: int, rating: Literal["again", "hard", "easy"] | None = Body(default=None, embed=True), db: Session = Depends(get_db)) -> CourseVocabularyResponse:
    item = db.get(CourseVocabularyItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Module 1 vocabulary item not found")
    now = datetime.now(timezone.utc)
    intervals = (1, 3, 7, 14, 30)
    item.review_count += 1
    if rating == "again":
        item.interval_days = 0
    elif rating == "hard":
        item.interval_days = max(1, min(30, item.interval_days // 2))
    elif rating == "easy":
        item.interval_days = min(30, max(3, item.interval_days * 2))
    else:
        item.interval_days = intervals[min(item.review_count - 1, len(intervals) - 1)]
    item.last_reviewed_at = now
    item.next_review_at = now + (timedelta(minutes=10) if rating == "again" else timedelta(days=item.interval_days))
    db.commit()
    db.refresh(item)
    return _vocabulary_response(item)
