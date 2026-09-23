from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.course_backup import CourseBackup, backup_summary, export_backup, restore_backup
from app.services.course_state import (
    COURSE_STATE_CONFLICT_DETAIL,
    COURSE_STATE_REVISION_REQUIRED_DETAIL,
    CourseStateConflictError,
    course_state_revision,
    decode_course_state,
    load_course_state,
    parse_course_state_revision,
)

router = APIRouter(prefix="/api/v1/course/backup", tags=["course"])
MAX_BACKUP_BYTES = 10 * 1024 * 1024


async def read_backup(request: Request) -> CourseBackup:
    data = bytearray()
    async for chunk in request.stream():
        data.extend(chunk)
        if len(data) > MAX_BACKUP_BYTES:
            raise HTTPException(413, "Резервная копия превышает 10 МБ.")
    try:
        return CourseBackup.model_validate_json(bytes(data))
    except (ValidationError, ValueError):
        raise HTTPException(422, "Неверный формат резервной копии, версия или связи записей.") from None


@router.get("")
def download_backup(db: Session = Depends(get_db)) -> CourseBackup:
    return export_backup(db)


@router.post("/validate")
def validate_backup(backup: CourseBackup = Depends(read_backup)) -> dict:
    return backup_summary(backup)


@router.post("/restore")
def import_backup(
    backup: CourseBackup = Depends(read_backup),
    state_revision: str | None = Header(default=None, alias="X-Course-State-Revision"),
    db: Session = Depends(get_db),
) -> dict:
    if state_revision is None:
        raise HTTPException(status_code=428, detail=COURSE_STATE_REVISION_REQUIRED_DETAIL)
    try:
        expected_revision = parse_course_state_revision(state_revision)
        restore_backup(db, backup, expected_revision)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="Некорректная revision прогресса.") from error
    except CourseStateConflictError as error:
        raise HTTPException(status_code=409, detail=COURSE_STATE_CONFLICT_DETAIL) from error
    stored = load_course_state(db)
    return {
        "restored": True,
        "revision": course_state_revision(stored),
        "state": decode_course_state(stored) if stored else None,
    }
