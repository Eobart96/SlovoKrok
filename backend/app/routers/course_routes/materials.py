from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    CourseExercise,
    CourseExerciseAttempt,
    CourseHomework,
    CourseHomeworkAttempt,
    CourseReading,
    CourseReadingAttempt,
)
from app.routers.course_routes.common import commit_course_change
from app.schemas.course import (
    CourseMaterialCollection,
    CourseMaterialExerciseItem,
    CourseMaterialHomeworkItem,
    CourseMaterialImportBucket,
    CourseMaterialImportResponse,
    CourseMaterialReadingItem,
    CourseTasksDeleteRequest,
    CourseTasksDeleteResponse,
)


router = APIRouter()


def _values(item: Any, fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: getattr(item, field) for field in fields}


EXERCISE_FIELDS = ("lesson_slug", "lesson_title", "question", "instruction", "theory_snapshot", "created_at")
READING_FIELDS = ("lesson_slug", "lesson_title", "title", "text", "instruction", "reference_answer", "created_at")
HOMEWORK_FIELDS = ("lesson_slug", "lesson_title", "title", "description", "focus_category", "theory_snapshot", "reference_answer", "created_at")


@router.get("/materials/export", response_model=CourseMaterialCollection)
def export_materials(db: Session = Depends(get_db)) -> CourseMaterialCollection:
    return CourseMaterialCollection(
        format="slovokrok-course-materials",
        version=1,
        exported_at=datetime.now(timezone.utc),
        exercises=[
            CourseMaterialExerciseItem.model_validate(_values(item, EXERCISE_FIELDS))
            for item in db.scalars(select(CourseExercise).order_by(CourseExercise.id)).all()
        ],
        readings=[
            CourseMaterialReadingItem.model_validate(_values(item, READING_FIELDS))
            for item in db.scalars(select(CourseReading).order_by(CourseReading.id)).all()
        ],
        homework=[
            CourseMaterialHomeworkItem.model_validate(_values(item, HOMEWORK_FIELDS))
            for item in db.scalars(select(CourseHomework).order_by(CourseHomework.id)).all()
        ],
    )


def _import_rows(db: Session, model: Any, fields: tuple[str, ...], rows: list[Any]) -> CourseMaterialImportBucket:
    key_fields = tuple(field for field in fields if field != "created_at")
    existing = {
        tuple(getattr(item, field) for field in key_fields)
        for item in db.scalars(select(model)).all()
    }
    imported = 0
    skipped = 0
    for row in rows:
        values = row.model_dump()
        key = tuple(values[field] for field in key_fields)
        if key in existing:
            skipped += 1
            continue
        db.add(model(**values))
        existing.add(key)
        imported += 1
    return CourseMaterialImportBucket(imported=imported, skipped=skipped, total=len(rows))


@router.post("/materials/import", response_model=CourseMaterialImportResponse)
def import_materials(collection: CourseMaterialCollection, db: Session = Depends(get_db)) -> CourseMaterialImportResponse:
    try:
        result = CourseMaterialImportResponse(
            exercises=_import_rows(db, CourseExercise, EXERCISE_FIELDS, collection.exercises),
            readings=_import_rows(db, CourseReading, READING_FIELDS, collection.readings),
            homework=_import_rows(db, CourseHomework, HOMEWORK_FIELDS, collection.homework),
        )
        commit_course_change(db)
        return result
    except Exception:
        db.rollback()
        raise


@router.delete("/materials", response_model=CourseTasksDeleteResponse)
def delete_all_course_tasks(request: CourseTasksDeleteRequest, db: Session = Depends(get_db)) -> CourseTasksDeleteResponse:
    counts = {
        "exercises_deleted": db.query(CourseExercise).count(),
        "exercise_attempts_deleted": db.query(CourseExerciseAttempt).count(),
        "readings_deleted": db.query(CourseReading).count(),
        "reading_attempts_deleted": db.query(CourseReadingAttempt).count(),
        "homework_deleted": db.query(CourseHomework).count(),
        "homework_attempts_deleted": db.query(CourseHomeworkAttempt).count(),
    }
    try:
        db.query(CourseExerciseAttempt).delete(synchronize_session=False)
        db.query(CourseReadingAttempt).delete(synchronize_session=False)
        db.query(CourseHomeworkAttempt).delete(synchronize_session=False)
        db.query(CourseExercise).delete(synchronize_session=False)
        db.query(CourseReading).delete(synchronize_session=False)
        db.query(CourseHomework).delete(synchronize_session=False)
        commit_course_change(db)
    except Exception:
        db.rollback()
        raise
    return CourseTasksDeleteResponse(deleted=True, **counts)
