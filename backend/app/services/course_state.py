import json
from hashlib import sha256
import re

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import CourseState, utc_now
from app.schemas.course import CourseStatePayload


CURRENT_COURSE_STATE_SCHEMA_VERSION = 2
COURSE_STATE_CONFLICT_DETAIL = "Прогресс уже изменён в другом сеансе. Загрузите более новую сохранённую версию."
COURSE_STATE_REVISION_REQUIRED_DETAIL = "Для записи прогресса требуется актуальная revision."


class CourseStateConflictError(RuntimeError):
    pass


def parse_course_state_revision(value: str) -> str | None:
    if value == "none":
        return None
    if re.fullmatch(r"[0-9a-f]{64}", value):
        return value
    raise ValueError("Invalid course state revision")


def load_course_state(db: Session) -> CourseState | None:
    return db.get(CourseState, 1)


def course_state_revision(state: CourseState | None) -> str | None:
    if state is None:
        return None
    updated_at = state.updated_at.isoformat() if state.updated_at else ""
    source = f"{state.schema_version}\0{updated_at}\0{state.state_json}".encode("utf-8")
    return sha256(source).hexdigest()


def assert_course_state_revision(db: Session, expected_revision: str | None) -> CourseState | None:
    state = load_course_state(db)
    if course_state_revision(state) != expected_revision:
        raise CourseStateConflictError("Course state was changed by another client")
    return state


def save_course_state(
    db: Session,
    payload: CourseStatePayload,
    expected_revision: str | None,
    *,
    commit: bool = True,
) -> CourseState:
    state = db.get(CourseState, 1)
    if state is None:
        if expected_revision is not None:
            raise CourseStateConflictError("Course state was created by another client")
        state = CourseState(
            id=1,
            schema_version=CURRENT_COURSE_STATE_SCHEMA_VERSION,
            state_json=payload.model_dump_json(exclude_none=True),
            updated_at=utc_now(),
        )
        db.add(state)
        try:
            db.flush()
        except IntegrityError as error:
            db.rollback()
            raise CourseStateConflictError("Course state was created by another client") from error
    else:
        if course_state_revision(state) != expected_revision:
            raise CourseStateConflictError("Course state was changed by another client")
        previous_json = state.state_json
        previous_updated_at = state.updated_at
        next_updated_at = utc_now()
        result = db.execute(
            update(CourseState)
            .where(
                CourseState.id == state.id,
                CourseState.schema_version == state.schema_version,
                CourseState.state_json == previous_json,
                CourseState.updated_at == previous_updated_at,
            )
            .values(
                schema_version=CURRENT_COURSE_STATE_SCHEMA_VERSION,
                state_json=payload.model_dump_json(exclude_none=True),
                updated_at=next_updated_at,
            )
        )
        if result.rowcount != 1:
            db.rollback()
            raise CourseStateConflictError("Course state was changed by another client")
        db.expire_all()
        state = db.get(CourseState, 1)
        if state is None:
            db.rollback()
            raise CourseStateConflictError("Course state disappeared during update")
    if commit:
        db.commit()
        db.refresh(state)
    return state


def decode_course_state(state: CourseState) -> CourseStatePayload:
    if state.schema_version not in {1, CURRENT_COURSE_STATE_SCHEMA_VERSION}:
        raise ValueError(f"Unsupported course state schema version: {state.schema_version}")
    return CourseStatePayload.model_validate(json.loads(state.state_json))
