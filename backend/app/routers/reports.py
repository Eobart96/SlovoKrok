import base64
import io
import zipfile
import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from app.config import get_settings

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])
_lock = threading.Lock()
MAX_STORAGE = 30_000_000


class ReportScreenshot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=255)
    mime: Literal["image/png", "image/jpeg", "image/webp"]
    data: str = Field(max_length=2_800_000)

    @model_validator(mode="after")
    def validate_image(self):
        raw = base64.b64decode(self.data, validate=True)
        valid = {
            "image/png": raw.startswith(b"\x89PNG\r\n\x1a\n"),
            "image/jpeg": raw.startswith(b"\xff\xd8\xff"),
            "image/webp": raw.startswith(b"RIFF") and raw[8:12] == b"WEBP",
        }
        if len(raw) > 2 * 1024 * 1024 or not valid[self.mime]:
            raise ValueError("Допустимы PNG, JPEG и WebP до 2 МБ")
        return self


class ClearReportsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirmation: Literal["delete-all-reports"]


class ReportLocation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    view: str | None = Field(default=None, max_length=60)
    module: str | None = Field(default=None, max_length=255)
    lesson: str | None = Field(default=None, max_length=255)
    step: int | None = Field(default=None, ge=1, le=10_001)
    task_type: str | None = Field(default=None, max_length=30)
    task_id: str | None = Field(default=None, max_length=160)
    task_title: str | None = Field(default=None, max_length=500)
    scope: str | None = Field(default=None, max_length=255)
    training_stage: str | None = Field(default=None, max_length=30)


class ReportInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    section: Literal["learning", "cheats", "exercises", "homework", "reading", "review", "vocabulary"]
    description: str = Field(min_length=5, max_length=4_000)
    location: ReportLocation | None = None
    screenshots: list[ReportScreenshot] = Field(default_factory=list, max_length=3)


class Report(ReportInput):
    id: str
    created_at: datetime


def _load(path) -> list[Report]:
    if not path.exists():
        return []
    if path.stat().st_size > MAX_STORAGE:
        raise ValueError("Report storage is too large")
    return TypeAdapter(list[Report]).validate_json(path.read_text(encoding="utf-8"))


def _write(path, reports):
    content = json.dumps([item.model_dump(mode="json") for item in reports], ensure_ascii=False, indent=2)
    if len(content.encode("utf-8")) > MAX_STORAGE:
        raise HTTPException(409, "Хранилище обращений заполнено. Скачайте архив и очистите список.")
    temporary_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as output:
            temporary_path = output.name
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


@router.get("/export")
def export_reports():
    reports = list_reports()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        lines = ["SlovoKrok — обращения об ошибках"]
        for index, report in enumerate(reports, 1):
            lines.extend(["", f"{index}. {report.section}", f"Номер: {report.id}", f"Дата: {report.created_at.isoformat()}"])
            if report.location:
                lines.extend(f"{key}: {value}" for key, value in report.location.model_dump().items() if value is not None)
            lines.append(report.description)
            for number, screenshot in enumerate(report.screenshots, 1):
                extension = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}[screenshot.mime]
                filename = f"screenshots/report_{index:03d}_{number}.{extension}"
                archive.writestr(filename, base64.b64decode(screenshot.data, validate=True))
                lines.append(f"Скриншот: {filename} ({screenshot.name})")
        archive.writestr("SlovoKrok_обращения.txt", "\ufeff" + "\n".join(lines))
    return {"data": base64.b64encode(output.getvalue()).decode("ascii")}


@router.delete("")
def clear_reports(request: ClearReportsInput):
    try:
        with _lock:
            path = get_settings().runtime_data_dir / "issue_reports.json"
            _load(path)
            _write(path, [])
        return {"deleted": True}
    except (OSError, ValueError) as error:
        raise HTTPException(503, "Не удалось очистить обращения.") from error


@router.get("", response_model=list[Report])
def list_reports() -> list[Report]:
    try:
        with _lock:
            return _load(get_settings().runtime_data_dir / "issue_reports.json")
    except (OSError, ValueError) as error:
        raise HTTPException(503, "Не удалось прочитать обращения. Сохранённый файл не изменён.") from error


@router.post("", response_model=Report, status_code=201)
def create_report(request: ReportInput) -> Report:
    try:
        with _lock:
            path = get_settings().runtime_data_dir / "issue_reports.json"
            reports = _load(path)
            if len(reports) >= 500:
                raise HTTPException(409, "Достигнут предел в 500 обращений. Новое обращение не сохранено.")
            report = Report(**request.model_dump(), id=str(uuid4()), created_at=datetime.now(timezone.utc))
            _write(path, [report, *reports])
            return report
    except (OSError, ValueError) as error:
        raise HTTPException(503, "Не удалось сохранить обращение. Попробуйте ещё раз.") from error
