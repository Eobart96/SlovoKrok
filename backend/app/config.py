from functools import lru_cache
import os
from pathlib import Path
import sys
from typing import Any

from pydantic import Field, PrivateAttr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def default_runtime_data_dir() -> Path:
    """Return the per-user application data directory without creating it."""
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return (base / "SlovoKrok").resolve()
    if sys.platform == "darwin":
        return (Path.home() / "Library" / "Application Support" / "SlovoKrok").resolve()
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return (base / "slovokrok").resolve()


def sqlite_url(path: Path) -> str:
    return f"sqlite:///{path.resolve().as_posix()}"


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    app_name: str = "SlovoKrok"
    runtime_data_dir: Path = Field(
        default_factory=default_runtime_data_dir,
        validation_alias="SLOVOKROK_DATA_DIR",
    )
    database_url: str = ""
    allow_project_database: bool = Field(
        default=False,
        validation_alias="SLOVOKROK_ALLOW_PROJECT_DATABASE",
    )
    learning_path: Path = PROJECT_ROOT / "course-content" / "slovak-a1" / "learning"
    project_root: Path = PROJECT_ROOT
    tutor_provider: str = "codex"
    codex_command: str = "codex.cmd"
    tutor_timeout_seconds: int = Field(default=120, ge=5, le=300)
    share_private_tutor_profile: bool = False
    openai_api_key: str | None = None
    openai_model: str = "gpt-5"
    polza_api_key: str | None = None
    polza_model: str = "openai/gpt-4o-mini"
    polza_base_url: str = "https://polza.ai/api/v1"

    _database_url_is_managed: bool = PrivateAttr(default=False)
    _legacy_database_path: Path | None = PrivateAttr(default=None)

    @field_validator("runtime_data_dir")
    @classmethod
    def validate_runtime_data_dir(cls, value: Path) -> Path:
        path = Path(value).expanduser()
        if not path.is_absolute():
            raise ValueError("SLOVOKROK_DATA_DIR must be an absolute path")
        return path.resolve()

    def model_post_init(self, __context: Any) -> None:
        if self.database_url.strip():
            self.database_url = self.database_url.strip()
            database_path = self._sqlite_database_path(self.database_url)
            if (
                database_path is None
                or self.allow_project_database
                or not database_path.is_relative_to(self.project_root.resolve())
            ):
                return
            self._legacy_database_path = database_path
        self.database_url = sqlite_url(self.runtime_data_dir / "app.db")
        self._database_url_is_managed = True

    @staticmethod
    def _sqlite_database_path(database_url: str) -> Path | None:
        prefix = "sqlite:///"
        if not database_url.startswith(prefix):
            return None
        raw_path = database_url.removeprefix(prefix)
        if raw_path == ":memory:":
            return None
        return Path(raw_path).expanduser().resolve()

    @property
    def database_url_is_managed(self) -> bool:
        return self._database_url_is_managed

    @property
    def legacy_database_path(self) -> Path | None:
        return self._legacy_database_path

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    from app.services.runtime_data import prepare_runtime_data
    from app.services.tutor_settings import apply_saved_tutor_settings

    prepare_runtime_data(settings)
    apply_saved_tutor_settings(settings)
    return settings
