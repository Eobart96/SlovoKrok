from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import tempfile

from sqlalchemy.engine import Connection, Engine

from app.database import Base, SQLITE_BUSY_TIMEOUT_MS, engine

# Importing models registers the active tables in SQLAlchemy metadata.
from app import models as _models  # noqa: F401


MIGRATION_TABLE = "slovokrok_schema_migrations"


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable[[Connection], None]


def _create_active_schema(connection: Connection) -> None:
    Base.metadata.create_all(bind=connection)


def _add_offline_answer_references(connection: Connection) -> None:
    for table in ("module1_beta_readings", "module1_beta_homework"):
        columns = {row[1] for row in connection.exec_driver_sql(f"PRAGMA table_info({table})").all()}
        if "reference_answer" not in columns:
            connection.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN reference_answer TEXT")


MIGRATIONS: tuple[Migration, ...] = (
    Migration(1, "create_active_schema", _create_active_schema),
    Migration(2, "add_offline_answer_references", _add_offline_answer_references),
)


def _quick_check(connection: Connection) -> None:
    results = [row[0] for row in connection.exec_driver_sql("PRAGMA quick_check").all()]
    if results != ["ok"]:
        raise RuntimeError(f"SQLite quick_check failed: {results[:3]}")


def _migration_rows(connection: Connection) -> list[tuple[int, str]]:
    exists = connection.exec_driver_sql(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (MIGRATION_TABLE,),
    ).first()
    if exists is None:
        return []
    return [tuple(row) for row in connection.exec_driver_sql(
        f"SELECT version, name FROM {MIGRATION_TABLE} ORDER BY version"
    ).all()]


def _validate_migration_history(rows: Sequence[tuple[int, str]], migrations: Sequence[Migration]) -> None:
    expected = [(migration.version, migration.name) for migration in migrations[:len(rows)]]
    if list(rows) != expected:
        raise RuntimeError(f"Unknown or inconsistent SQLite migration history: {list(rows)}")


def _database_path(database_engine: Engine) -> Path | None:
    if database_engine.dialect.name != "sqlite":
        return None
    database = database_engine.url.database
    if not database or database == ":memory:":
        return None
    return Path(database).resolve()


def _validate_backup(path: Path) -> None:
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True, timeout=5)
    try:
        if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise RuntimeError(f"SQLite migration backup is corrupt: {path}")
    finally:
        connection.close()


def _backup_before_migrations(database_path: Path, current: int, target: int) -> Path | None:
    if not database_path.is_file() or database_path.stat().st_size == 0:
        return None
    backup_path = database_path.with_name(
        f"{database_path.name}.pre-migration-v{current}-to-v{target}.bak"
    )
    if backup_path.exists():
        _validate_backup(backup_path)
        return backup_path
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{backup_path.name}.", suffix=".tmp", dir=database_path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    source: sqlite3.Connection | None = None
    destination: sqlite3.Connection | None = None
    try:
        source = sqlite3.connect(f"{database_path.as_uri()}?mode=ro", uri=True, timeout=5)
        destination = sqlite3.connect(temporary)
        source.backup(destination)
        destination.commit()
        destination.close()
        destination = None
        _validate_backup(temporary)
        try:
            os.link(temporary, backup_path)
        except FileExistsError:
            _validate_backup(backup_path)
        return backup_path
    finally:
        if destination is not None:
            destination.close()
        if source is not None:
            source.close()
        temporary.unlink(missing_ok=True)


def run_migrations(connection: Connection, migrations: Sequence[Migration] = MIGRATIONS) -> None:
    versions = [migration.version for migration in migrations]
    if versions != list(range(1, len(migrations) + 1)) or len(set(versions)) != len(versions):
        raise RuntimeError("SQLite migrations must use contiguous unique versions starting at 1")
    if connection.in_transaction():
        connection.commit()
    connection.exec_driver_sql("BEGIN IMMEDIATE")
    try:
        connection.exec_driver_sql(
            f"CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} ("
            "version INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, applied_at TEXT NOT NULL)"
        )
        rows = _migration_rows(connection)
        _validate_migration_history(rows, migrations)
        for migration in migrations[len(rows):]:
            migration.apply(connection)
            connection.exec_driver_sql(
                f"INSERT INTO {MIGRATION_TABLE}(version, name, applied_at) VALUES (?, ?, ?)",
                (migration.version, migration.name, datetime.now(timezone.utc).isoformat()),
            )
        _quick_check(connection)
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def initialize_application(database_engine: Engine | None = None) -> None:
    """Validate, back up, and migrate the active database without touching legacy sources."""
    active_engine = database_engine if database_engine is not None else engine
    if active_engine.dialect.name != "sqlite":
        Base.metadata.create_all(bind=active_engine)
        return

    with active_engine.connect() as connection:
        _quick_check(connection)
        rows = _migration_rows(connection)
        _validate_migration_history(rows, MIGRATIONS)
        current_version = len(rows)
    if current_version < len(MIGRATIONS):
        database_path = _database_path(active_engine)
        if database_path is not None:
            _backup_before_migrations(database_path, current_version, len(MIGRATIONS))

    with active_engine.connect() as connection:
        if _database_path(active_engine) is not None:
            journal_mode = connection.exec_driver_sql("PRAGMA journal_mode=WAL").scalar_one()
            if str(journal_mode).lower() != "wal":
                raise RuntimeError(f"SQLite refused WAL journal mode: {journal_mode}")
            connection.commit()
        run_migrations(connection)
        if connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() != 1:
            raise RuntimeError("SQLite foreign keys are not enabled")
        if connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() != SQLITE_BUSY_TIMEOUT_MS:
            raise RuntimeError("SQLite busy timeout is not configured")
        _quick_check(connection)
