import json
from pathlib import Path
import sqlite3

import pytest
from pydantic import ValidationError

from app.config import Settings, sqlite_url
from app.services.runtime_data import prepare_runtime_data
from app.services.tutor_settings import settings_file


def _settings(tmp_path: Path, **overrides) -> Settings:
    values = {
        "project_root": tmp_path / "project",
        "runtime_data_dir": tmp_path / "local-data",
        "database_url": "",
        "learning_path": tmp_path / "learning",
        "_env_file": None,
    }
    values.update(overrides)
    return Settings(**values)


def _create_legacy_database(path: Path, value: str = "preserved") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE migration_probe (value TEXT NOT NULL)")
    connection.execute("INSERT INTO migration_probe(value) VALUES (?)", (value,))
    connection.commit()
    connection.close()


def _read_probe(path: Path) -> str:
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    value = connection.execute("SELECT value FROM migration_probe").fetchone()[0]
    connection.close()
    return value


def test_managed_database_uses_runtime_data_directory(tmp_path: Path):
    settings = _settings(tmp_path)

    assert settings.database_url_is_managed is True
    assert settings.database_url == sqlite_url(settings.runtime_data_dir / "app.db")
    assert settings_file(settings) == settings.runtime_data_dir / "ai_settings.json"


def test_environment_override_sets_managed_runtime_paths(tmp_path: Path, monkeypatch):
    override = (tmp_path / "environment-data").resolve()
    monkeypatch.setenv("SLOVOKROK_DATA_DIR", str(override))

    settings = Settings(database_url="", _env_file=None)

    assert settings.runtime_data_dir == override
    assert settings.database_url == sqlite_url(override / "app.db")
    assert settings_file(settings) == override / "ai_settings.json"


def test_runtime_data_directory_must_be_absolute():
    with pytest.raises(ValidationError, match="absolute path"):
        Settings(runtime_data_dir=Path("relative-data"), _env_file=None)


def test_legacy_database_and_settings_are_copied_without_deleting_sources(tmp_path: Path):
    settings = _settings(tmp_path)
    legacy = settings.project_root / "backend" / "data"
    legacy_database = legacy / "app.db"
    legacy_settings = legacy / "ai_settings.json"
    _create_legacy_database(legacy_database)
    legacy_settings.write_text(json.dumps({"tutor_provider": "codex", "test_value": "kept"}), encoding="utf-8")

    result = prepare_runtime_data(settings)

    assert result.database == "copied"
    assert result.tutor_settings == "copied"
    assert legacy_database.is_file()
    assert legacy_settings.is_file()
    assert _read_probe(settings.runtime_data_dir / "app.db") == "preserved"
    assert json.loads(settings_file(settings).read_text(encoding="utf-8"))["test_value"] == "kept"


def test_existing_destination_is_never_overwritten(tmp_path: Path):
    settings = _settings(tmp_path)
    legacy_database = settings.project_root / "backend" / "data" / "app.db"
    destination = settings.runtime_data_dir / "app.db"
    _create_legacy_database(legacy_database, "legacy")
    _create_legacy_database(destination, "current")

    result = prepare_runtime_data(settings)

    assert result.database == "destination_exists"
    assert _read_probe(destination) == "current"
    assert _read_probe(legacy_database) == "legacy"


def test_corrupt_legacy_database_is_not_published(tmp_path: Path):
    settings = _settings(tmp_path)
    legacy_database = settings.project_root / "backend" / "data" / "app.db"
    legacy_database.parent.mkdir(parents=True)
    legacy_database.write_bytes(b"not a sqlite database")

    with pytest.raises(RuntimeError, match="Could not copy legacy SQLite"):
        prepare_runtime_data(settings)

    assert legacy_database.is_file()
    assert not (settings.runtime_data_dir / "app.db").exists()


def test_explicit_database_url_skips_database_copy_but_keeps_settings_migration(tmp_path: Path):
    custom_database = tmp_path / "custom" / "custom.db"
    settings = _settings(tmp_path, database_url=sqlite_url(custom_database))
    legacy = settings.project_root / "backend" / "data"
    _create_legacy_database(legacy / "app.db")
    legacy.mkdir(parents=True, exist_ok=True)
    (legacy / "ai_settings.json").write_text('{"tutor_provider":"codex"}', encoding="utf-8")

    result = prepare_runtime_data(settings)

    assert settings.database_url_is_managed is False
    assert result.database == "custom_database_url"
    assert result.tutor_settings == "copied"
    assert not (settings.runtime_data_dir / "app.db").exists()


def test_project_local_database_url_is_treated_as_legacy_source(tmp_path: Path):
    project_root = tmp_path / "project"
    legacy_database = project_root / "backend" / "app.db"
    settings = _settings(
        tmp_path,
        project_root=project_root,
        database_url=sqlite_url(legacy_database),
    )
    _create_legacy_database(legacy_database, "project-local")

    result = prepare_runtime_data(settings)

    assert settings.database_url_is_managed is True
    assert settings.legacy_database_path == legacy_database.resolve()
    assert settings.database_url == sqlite_url(settings.runtime_data_dir / "app.db")
    assert result.database == "copied"
    assert _read_probe(legacy_database) == "project-local"
    assert _read_probe(settings.runtime_data_dir / "app.db") == "project-local"


def test_project_local_database_requires_explicit_rollback_opt_in(tmp_path: Path):
    project_root = tmp_path / "project"
    legacy_database = project_root / "backend" / "app.db"
    settings = _settings(
        tmp_path,
        project_root=project_root,
        database_url=sqlite_url(legacy_database),
        allow_project_database=True,
    )

    result = prepare_runtime_data(settings)

    assert settings.database_url_is_managed is False
    assert settings.legacy_database_path is None
    assert settings.database_url == sqlite_url(legacy_database)
    assert result.database == "custom_database_url"


def test_legacy_directory_can_be_used_as_explicit_rollback_location(tmp_path: Path):
    legacy = tmp_path / "project" / "backend" / "data"
    settings = _settings(tmp_path, runtime_data_dir=legacy)
    _create_legacy_database(legacy / "app.db")
    (legacy / "ai_settings.json").write_text('{"tutor_provider":"codex"}', encoding="utf-8")

    result = prepare_runtime_data(settings)

    assert result.database == "same_path"
    assert result.tutor_settings == "same_path"
    assert _read_probe(legacy / "app.db") == "preserved"
