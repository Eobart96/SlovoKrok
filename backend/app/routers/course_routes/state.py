from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseStatePayload, CourseStateResponse
from app.services.course_state import (
    COURSE_STATE_CONFLICT_DETAIL,
    COURSE_STATE_REVISION_REQUIRED_DETAIL,
    CourseStateConflictError,
    course_state_revision,
    decode_course_state,
    load_course_state,
    parse_course_state_revision,
    save_course_state,
)


router = APIRouter()


@router.get("/state", response_model=CourseStateResponse)
def get_state(db: Session = Depends(get_db)) -> CourseStateResponse:
    stored = load_course_state(db)
    if stored is None:
        return CourseStateResponse(exists=False)
    return CourseStateResponse(
        exists=True,
        schema_version=stored.schema_version,
        revision=course_state_revision(stored),
        state=decode_course_state(stored),
        updated_at=stored.updated_at,
    )


@router.put("/state", response_model=CourseStateResponse)
def put_state(
    payload: CourseStatePayload,
    state_revision: str | None = Header(default=None, alias="X-Course-State-Revision"),
    db: Session = Depends(get_db),
) -> CourseStateResponse:
    if state_revision is None:
        raise HTTPException(status_code=428, detail=COURSE_STATE_REVISION_REQUIRED_DETAIL)
    try:
        expected_revision = parse_course_state_revision(state_revision)
        stored = save_course_state(db, payload, expected_revision)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="Некорректная revision прогресса.") from error
    except CourseStateConflictError as error:
        raise HTTPException(status_code=409, detail=COURSE_STATE_CONFLICT_DETAIL) from error
    return CourseStateResponse(
        exists=True,
        schema_version=stored.schema_version,
        revision=course_state_revision(stored),
        state=decode_course_state(stored),
        updated_at=stored.updated_at,
    )
