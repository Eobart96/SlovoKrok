from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from app.config import Settings


MigrationStatus = Literal[
    "copied",
    "destination_exists",
    "legacy_missing",
    "same_path",
    "custom_database_url",
]


@dataclass(frozen=True)
class RuntimeMigrationResult:
    database: MigrationStatus
    tutor_settings: MigrationStatus


def legacy_data_dir(settings: "Settings") -> Path:
    return settings.project_root / "backend" / "data"


def prepare_runtime_data(settings: "Settings") -> RuntimeMigrationResult:
    """Prepare local runtime storage and copy legacy files without deleting them."""
    settings.runtime_data_dir.mkdir(parents=True, exist_ok=True)
    legacy = legacy_data_dir(settings)
    database_status: MigrationStatus = "custom_database_url"
    if settings.database_url_is_managed:
        source_database = settings.legacy_database_path or legacy / "app.db"
        database_status = _copy_sqlite_database(source_database, settings.runtime_data_dir / "app.db")
    settings_status = _copy_regular_file(
        legacy / "ai_settings.json",
        settings.runtime_data_dir / "ai_settings.json",
    )
    return RuntimeMigrationResult(database=database_status, tutor_settings=settings_status)


def _same_path(source: Path, destination: Path) -> bool:
    return source.resolve() == destination.resolve()


def _validate_legacy_source(source: Path) -> None:
    if source.is_symlink():
        raise RuntimeError(f"Refusing to migrate a symbolic link: {source}")


def _publish_without_overwrite(temporary: Path, destination: Path) -> MigrationStatus:
    try:
        os.link(temporary, destination)
        return "copied"
    except FileExistsError:
        return "destination_exists"
    finally:
        temporary.unlink(missing_ok=True)


def _copy_regular_file(source: Path, destination: Path) -> MigrationStatus:
    if _same_path(source, destination):
        return "same_path"
    if destination.exists():
        return "destination_exists"
    if not source.is_file():
        return "legacy_missing"
    _validate_legacy_source(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".migrating",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with source.open("rb") as reader, os.fdopen(descriptor, "wb") as writer:
            shutil.copyfileobj(reader, writer)
            writer.flush()
            os.fsync(writer.fileno())
        return _publish_without_overwrite(temporary, destination)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise


def _copy_sqlite_database(source: Path, destination: Path) -> MigrationStatus:
    if _same_path(source, destination):
        return "same_path"
    if destination.exists():
        return "destination_exists"
    if not source.is_file():
        return "legacy_missing"
    _validate_legacy_source(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".migrating",
        dir=destination.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    source_connection: sqlite3.Connection | None = None
    target_connection: sqlite3.Connection | None = None
    try:
        source_connection = sqlite3.connect(f"{source.resolve().as_uri()}?mode=ro", uri=True, timeout=10)
        if source_connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise RuntimeError("Legacy SQLite integrity check failed")
        target_connection = sqlite3.connect(temporary)
        source_connection.backup(target_connection)
        if target_connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise RuntimeError("Copied SQLite integrity check failed")
        if source_connection.execute("PRAGMA page_count").fetchone()[0] != target_connection.execute("PRAGMA page_count").fetchone()[0]:
            raise RuntimeError("Copied SQLite page count does not match the legacy database")
        target_connection.close()
        target_connection = None
        source_connection.close()
        source_connection = None
        return _publish_without_overwrite(temporary, destination)
    except (OSError, sqlite3.DatabaseError, RuntimeError) as error:
        raise RuntimeError(f"Could not copy legacy SQLite database: {error}") from error
    finally:
        if target_connection is not None:
            target_connection.close()
        if source_connection is not None:
            source_connection.close()
        temporary.unlink(missing_ok=True)
