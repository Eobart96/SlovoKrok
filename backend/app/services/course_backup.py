"""Portable, validated course backup. Never reads provider settings or files."""
import json
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas.course import CourseStatePayload
from app.services.course_state import (
    assert_course_state_revision,
    decode_course_state,
    load_course_state,
    save_course_state,
)


# Names in the portable format are independent of physical SQLite table names.
TABLES = {
    "exercises": models.CourseExercise,
    "exercise_attempts": models.CourseExerciseAttempt,
    "readings": models.CourseReading,
    "reading_attempts": models.CourseReadingAttempt,
    "vocabulary": models.CourseVocabularyItem,
    "homework": models.CourseHomework,
    "homework_attempts": models.CourseHomeworkAttempt,
    "translation_history": models.TranslationHistoryEntry,
    "translation_questions": models.TranslationHistoryQuestion,
}
VERSION_1_TABLES = set(TABLES) - {"translation_history", "translation_questions"}
RELATIONS = {
    "exercise_attempts": ("exercise_id", "exercises"),
    "reading_attempts": ("reading_id", "readings"),
    "homework_attempts": ("homework_id", "homework"),
    "translation_questions": ("translation_id", "translation_history"),
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


def _validate_translation_backup_row(name: str, row: dict[str, Any]) -> None:
    def require_text(field: str, maximum: int) -> None:
        value = row[field]
        if not isinstance(value, str) or not 1 <= len(value) <= maximum:
            raise ValueError(f"Invalid {name}.{field}")

    if name == "translation_history":
        if row["direction"] not in {"ru-sk", "sk-ru"}:
            raise ValueError("Invalid translation history direction")
        require_text("source_text", 2_000)
        require_text("translation", 4_000)
        require_text("provider", 40)
        if row["note"] is not None and (not isinstance(row["note"], str) or len(row["note"]) > 500):
            raise ValueError("Invalid translation history note")
        try:
            alternatives = json.loads(row["alternatives_json"])
        except (json.JSONDecodeError, TypeError) as error:
            raise ValueError("Invalid translation history alternatives") from error
        if (
            not isinstance(alternatives, list)
            or len(alternatives) > 2
            or any(not isinstance(item, str) or not 1 <= len(item) <= 4_000 for item in alternatives)
        ):
            raise ValueError("Invalid translation history alternatives")
    elif name == "translation_questions":
        require_text("question", 1_000)
        require_text("answer", 4_000)
        require_text("provider", 40)


class BackupState(CourseStatePayload):
    model_config = ConfigDict(extra="forbid")


class CourseBackup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: Literal["slovokrok-course-backup"]
    version: Literal[1, 2]
    exported_at: datetime
    state: BackupState | None
    tables: dict[str, list[dict[str, Any]]]

    @model_validator(mode="after")
    def validate_tables(self):
        expected_tables = VERSION_1_TABLES if self.version == 1 else set(TABLES)
        if set(self.tables) != expected_tables:
            raise ValueError("Unexpected backup tables")
        for name, rows in self.tables.items():
            if len(rows) > 20_000:
                raise ValueError("Too many backup records")
            normalized = [ROW_SCHEMAS[name].model_validate(row).model_dump() for row in rows]
            if len({row["id"] for row in normalized}) != len(normalized):
                raise ValueError("Duplicate backup identifiers")
            for row in normalized:
                _validate_translation_backup_row(name, row)
            self.tables[name] = normalized
        vocabulary_keys = [(row["lesson_slug"], row["word"]) for row in self.tables["vocabulary"]]
        if len(set(vocabulary_keys)) != len(vocabulary_keys):
            raise ValueError("Duplicate vocabulary entries")
        for name, (field, parent) in RELATIONS.items():
            if name not in self.tables:
                continue
            parent_ids = {row["id"] for row in self.tables[parent]}
            if any(row[field] not in parent_ids for row in self.tables[name]):
                raise ValueError("Broken backup relationship")
        return self


def export_backup(db: Session) -> CourseBackup:
    stored = load_course_state(db)
    return CourseBackup(
        format="slovokrok-course-backup", version=2,
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


def restore_backup(db: Session, backup: CourseBackup, expected_revision: str | None) -> None:
    """Add materials, preserving existing records; restore state atomically.

    Reimporting an identical archive is idempotent. Foreign keys are remapped,
    and an existing vocabulary card keeps its current review history.
    """
    remaps: dict[str, dict[int, int]] = {}
    try:
        assert_course_state_revision(db, expected_revision)
        for name, model in TABLES.items():
            if name not in backup.tables:
                continue
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
            save_course_state(db, backup.state, expected_revision, commit=False)
        db.commit()
    except Exception:
        db.rollback()
        raise
