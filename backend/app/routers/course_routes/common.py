from collections.abc import Callable
from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.tutor import (
    AI_INVALID_RESPONSE_DETAIL,
    AI_PROVIDER_TIMEOUT_DETAIL,
    AI_PROVIDER_UNAVAILABLE_DETAIL,
    AIResponseError,
    TutorProviderError,
    TutorProviderTimeout,
)


ResultT = TypeVar("ResultT")
COURSE_STORAGE_UNAVAILABLE_DETAIL = "Не удалось сохранить задания в локальной базе"


def invoke_tutor(operation: Callable[[], ResultT]) -> ResultT:
    """Map all provider failures to the stable public HTTP contract."""
    try:
        return operation()
    except AIResponseError as error:
        raise HTTPException(status_code=502, detail=AI_INVALID_RESPONSE_DETAIL) from error
    except TutorProviderTimeout as error:
        raise HTTPException(status_code=504, detail=AI_PROVIDER_TIMEOUT_DETAIL) from error
    except (TutorProviderError, FileNotFoundError, RuntimeError, TimeoutError) as error:
        raise HTTPException(status_code=503, detail=AI_PROVIDER_UNAVAILABLE_DETAIL) from error


def commit_course_change(db: Session) -> None:
    """Rollback failed task writes and expose a stable non-500 response."""
    try:
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=503, detail=COURSE_STORAGE_UNAVAILABLE_DETAIL) from error
