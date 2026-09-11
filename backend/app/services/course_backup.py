"""Portable, validated course backup. Never reads provider settings or files."""
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas.course import CourseStatePayload
from app.services.course_state import decode_course_state, load_course_state


# Names in the portable format are independent of physical SQLite table names.
TABLES = {
    "exercises": models.CourseExercise,
    "exercise_attempts": models.CourseExerciseAttempt,
    "readings": models.CourseReading,
    "reading_attempts": models.CourseReadingAttempt,
    "vocabulary": models.CourseVocabularyItem,
    "homework": models.CourseHomework,
    "homework_attempts": models.CourseHomeworkAttempt,
}
RELATIONS = {
    "exercise_attempts": ("exercise_id", "exercises"),
    "reading_attempts": ("reading_id", "readings"),
    "homework_attempts": ("homework_id", "homework"),
}


def _row_schema(name, model):
    fields = {}
    for column in model.__table__.columns:
        kind = column.type.python_type
        options = {}
        if kind is str:
            options["max_length"] = getattr(column.type, "length", None) or 100_000
        if kind is int:
            options["ge"] = 1 if column.name == "id" or column.foreign_keys else 0
            if column.name == "score":
                options["le"] = 100
        fields[column.name] = (kind | None if column.nullable else kind, Field(..., **options))
    return create_model(f"Backup_{name}", __config__=ConfigDict(extra="forbid"), **fields)


ROW_SCHEMAS = {name: _row_schema(name, model) for name, model in TABLES.items()}


class BackupState(CourseStatePayload):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def valid_progress(self):
        if any(value not in {"not_started", "in_progress", "completed"} for value in self.progress.values()):
            raise ValueError("Unknown progress status")
        if any(value < 0 for value in self.lessonSteps.values()):
            raise ValueError("Negative lesson step")
        for mistake in self.mistakes.values():
            for key in ("id", "lessonSlug", "prompt", "answer"):
                if not isinstance(mistake.get(key), str):
                    raise ValueError("Invalid mistake record")
            if not isinstance(mistake.get("mastered"), bool):
                raise ValueError("Invalid mistake status")
        for summary in self.lessonSummaries.values():
            if not isinstance(summary.get("understanding"), (int, float)) or not isinstance(summary.get("level"), str):
                raise ValueError("Invalid lesson summary")
            for key in ("strengths", "review"):
                if not isinstance(summary.get(key), list) or not all(isinstance(item, str) for item in summary[key]):
                    raise ValueError("Invalid lesson summary list")
        return self


class CourseBackup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: Literal["slovokrok-course-backup"]
    version: Literal[1]
    exported_at: datetime
    state: BackupState | None
    tables: dict[str, list[dict[str, Any]]]

    @model_validator(mode="after")
    def validate_tables(self):
        if set(self.tables) != set(TABLES):
            raise ValueError("Unexpected backup tables")
        for name, rows in self.tables.items():
            if len(rows) > 20_000:
                raise ValueError("Too many backup records")
            normalized = [ROW_SCHEMAS[name].model_validate(row).model_dump() for row in rows]
            if len({row["id"] for row in normalized}) != len(normalized):
                raise ValueError("Duplicate backup identifiers")
            self.tables[name] = normalized
        vocabulary_keys = [(row["lesson_slug"], row["word"]) for row in self.tables["vocabulary"]]
        if len(set(vocabulary_keys)) != len(vocabulary_keys):
            raise ValueError("Duplicate vocabulary entries")
        for name, (field, parent) in RELATIONS.items():
            parent_ids = {row["id"] for row in self.tables[parent]}
            if any(row[field] not in parent_ids for row in self.tables[name]):
                raise ValueError("Broken backup relationship")
        return self


def export_backup(db: Session) -> CourseBackup:
    stored = load_course_state(db)
    return CourseBackup(
        format="slovokrok-course-backup", version=1,
        exported_at=datetime.now(timezone.utc),
        state=BackupState.model_validate(decode_course_state(stored).model_dump()) if stored else None,
        tables={name: [
            {column.name: getattr(row, column.name) for column in model.__table__.columns}
            for row in db.scalars(select(model).order_by(model.id)).all()
        ] for name, model in TABLES.items()},
    )


def backup_summary(backup: CourseBackup) -> dict:
    return {"exported_at": backup.exported_at, "has_state": backup.state is not None,
            "completed_topics": sum(value == "completed" for value in backup.state.progress.values()) if backup.state else 0,
            "counts": {name: len(rows) for name, rows in backup.tables.items()}}


def restore_backup(db: Session, backup: CourseBackup) -> None:
    """Add materials, preserving existing records; restore state atomically.

    Reimporting an identical archive is idempotent. Foreign keys are remapped,
    and an existing vocabulary card keeps its current review history.
    """
    remaps: dict[str, dict[int, int]] = {}
    try:
        for name, model in TABLES.items():
            remaps[name] = {}
            for row in backup.tables[name]:
                values = {key: value for key, value in row.items() if key != "id"}
                if name in RELATIONS:
                    field, parent = RELATIONS[name]
                    values[field] = remaps[parent][values[field]]
                match = {key: values[key] for key in ("lesson_slug", "word")} if name == "vocabulary" else values
                existing = db.scalar(select(model).filter_by(**match).limit(1))
                if existing is None:
                    existing = model(**values)
                    db.add(existing)
                    db.flush()
                remaps[name][row["id"]] = existing.id
        if backup.state is not None:
            stored = load_course_state(db)
            if stored is None:
                stored = models.CourseState(id=1)
                db.add(stored)
            stored.schema_version = 1
            stored.state_json = backup.state.model_dump_json()
            stored.updated_at = models.utc_now()
        db.commit()
    except Exception:
        db.rollback()
        raise
