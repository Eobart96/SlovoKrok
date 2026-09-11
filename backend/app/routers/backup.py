from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.course_backup import CourseBackup, backup_summary, export_backup, restore_backup
from app.services.course_state import decode_course_state, load_course_state

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
def import_backup(backup: CourseBackup = Depends(read_backup), db: Session = Depends(get_db)) -> dict:
    restore_backup(db, backup)
    stored = load_course_state(db)
    return {"restored": True, "state": decode_course_state(stored) if stored else None}
