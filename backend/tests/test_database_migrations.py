from contextlib import closing
from hashlib import sha256
from pathlib import Path
import shutil
import sqlite3

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import SQLITE_BUSY_TIMEOUT_MS, create_database_engine
from app.models import CourseExerciseAttempt
from app.services.startup import MIGRATION_TABLE, Migration, initialize_application, run_migrations


def _database_url(path: Path) -> str:
    return f"sqlite:///{path.as_posix()}"


def _create_legacy_database(path: Path) -> None:
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE module1_beta_state ("
        "id INTEGER PRIMARY KEY, schema_version INTEGER NOT NULL, "
        "state_json TEXT NOT NULL, updated_at DATETIME)"
    )
    connection.execute(
        "INSERT INTO module1_beta_state(id, schema_version, state_json, updated_at) "
        "VALUES (1, 1, ?, ?)",
        ('{"currentLesson":"legacy"}', "2026-01-01 00:00:00"),
    )
    connection.execute("CREATE TABLE legacy_probe (value TEXT NOT NULL)")
    connection.execute("INSERT INTO legacy_probe(value) VALUES ('preserved')")
    connection.commit()
    connection.close()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_startup_configures_sqlite_and_enforces_foreign_keys(tmp_path: Path):
    database_path = tmp_path / "configured.db"
    database_engine = create_database_engine(_database_url(database_path))

    initialize_application(database_engine)

    with database_engine.connect() as connection:
        assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
        assert connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() == SQLITE_BUSY_TIMEOUT_MS
        assert connection.exec_driver_sql("PRAGMA journal_mode").scalar_one().lower() == "wal"
        assert connection.exec_driver_sql("PRAGMA quick_check").scalar_one() == "ok"

    with Session(database_engine) as session:
        session.add(CourseExerciseAttempt(
            exercise_id=999,
            answer="answer",
            is_correct=False,
            score=0,
            corrected_answer="corrected",
            explanation="explanation",
            next_exercise="next",
        ))
        with pytest.raises(IntegrityError):
            session.commit()
    database_engine.dispose()


def test_opening_connection_does_not_change_persistent_database_state(tmp_path: Path):
    database_path = tmp_path / "read-only-behavior.db"
    with closing(sqlite3.connect(database_path)) as connection, connection:
        connection.execute("CREATE TABLE sentinel (value TEXT NOT NULL)")
        connection.execute("INSERT INTO sentinel(value) VALUES ('preserved')")
        assert connection.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
    original_hash = _sha256(database_path)
    database_engine = create_database_engine(_database_url(database_path))

    with database_engine.connect() as connection:
        assert connection.exec_driver_sql("SELECT value FROM sentinel").scalar_one() == "preserved"
        assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
        assert connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() == SQLITE_BUSY_TIMEOUT_MS
        assert connection.exec_driver_sql("PRAGMA journal_mode").scalar_one() == "delete"
        assert connection.exec_driver_sql(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (MIGRATION_TABLE,)
        ).first() is None

    database_engine.dispose()
    assert _sha256(database_path) == original_hash


def test_legacy_copy_is_upgraded_idempotently_without_changing_source(tmp_path: Path):
    legacy_path = tmp_path / "legacy.db"
    upgraded_path = tmp_path / "upgraded.db"
    _create_legacy_database(legacy_path)
    source_hash = _sha256(legacy_path)
    shutil.copy2(legacy_path, upgraded_path)
    database_engine = create_database_engine(_database_url(upgraded_path))

    initialize_application(database_engine)
    initialize_application(database_engine)

    with database_engine.connect() as connection:
        state = connection.exec_driver_sql(
            "SELECT schema_version, state_json FROM module1_beta_state WHERE id=1"
        ).one()
        probe = connection.exec_driver_sql("SELECT value FROM legacy_probe").scalar_one()
        migrations = connection.exec_driver_sql(
            f"SELECT version, name FROM {MIGRATION_TABLE} ORDER BY version"
        ).all()
        assert tuple(state) == (1, '{"currentLesson":"legacy"}')
        assert probe == "preserved"
        assert migrations == [
            (1, "create_active_schema"),
            (2, "add_offline_answer_references"),
        ]
        reading_columns = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info(module1_beta_readings)").all()}
        homework_columns = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info(module1_beta_homework)").all()}
        assert "reference_answer" in reading_columns
        assert "reference_answer" in homework_columns
        assert connection.exec_driver_sql("PRAGMA quick_check").scalar_one() == "ok"

    backup_path = tmp_path / "upgraded.db.pre-migration-v0-to-v2.bak"
    assert backup_path.is_file()
    with closing(sqlite3.connect(f"{backup_path.resolve().as_uri()}?mode=ro", uri=True)) as backup, backup:
        assert backup.execute("SELECT value FROM legacy_probe").fetchone()[0] == "preserved"
        assert backup.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (MIGRATION_TABLE,)
        ).fetchone() is None

    database_engine.dispose()
    assert _sha256(legacy_path) == source_hash
    with closing(sqlite3.connect(f"{legacy_path.resolve().as_uri()}?mode=ro", uri=True)) as source, source:
        assert source.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (MIGRATION_TABLE,)
        ).fetchone() is None


def test_failed_migration_rolls_back_schema_data_and_history(tmp_path: Path):
    database_path = tmp_path / "rollback.db"
    database_engine = create_database_engine(_database_url(database_path))

    def create_probe(connection) -> None:
        connection.exec_driver_sql("CREATE TABLE rollback_probe (value TEXT NOT NULL)")
        connection.exec_driver_sql("INSERT INTO rollback_probe(value) VALUES ('first')")

    def fail_after_write(connection) -> None:
        connection.exec_driver_sql("INSERT INTO rollback_probe(value) VALUES ('second')")
        raise RuntimeError("forced migration failure")

    migrations = (
        Migration(1, "create_probe", create_probe),
        Migration(2, "fail_after_write", fail_after_write),
    )
    with database_engine.connect() as connection:
        with pytest.raises(RuntimeError, match="forced migration failure"):
            run_migrations(connection, migrations)

    with closing(sqlite3.connect(database_path)) as connection, connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert "rollback_probe" not in tables
        assert MIGRATION_TABLE not in tables
        assert connection.execute("PRAGMA quick_check").fetchone()[0] == "ok"
    database_engine.dispose()


def test_unknown_migration_history_is_rejected_without_rewriting_data(tmp_path: Path):
    database_path = tmp_path / "unknown-history.db"
    with closing(sqlite3.connect(database_path)) as connection, connection:
        connection.execute(
            f"CREATE TABLE {MIGRATION_TABLE} ("
            "version INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, applied_at TEXT NOT NULL)"
        )
        connection.execute(
            f"INSERT INTO {MIGRATION_TABLE}(version, name, applied_at) VALUES (99, 'unknown', 'now')"
        )
        connection.execute("CREATE TABLE sentinel (value TEXT NOT NULL)")
        connection.execute("INSERT INTO sentinel(value) VALUES ('preserved')")
    original_hash = _sha256(database_path)
    database_engine = create_database_engine(_database_url(database_path))

    with pytest.raises(RuntimeError, match="Unknown or inconsistent"):
        initialize_application(database_engine)

    database_engine.dispose()
    assert _sha256(database_path) == original_hash
