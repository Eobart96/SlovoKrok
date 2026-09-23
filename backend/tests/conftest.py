import atexit
from collections.abc import Generator
import os
from pathlib import Path
import shutil
import tempfile

_TEST_RUNTIME_DATA = Path(tempfile.mkdtemp(prefix="slovokrok-tests-"))
os.environ["SLOVOKROK_DATA_DIR"] = str(_TEST_RUNTIME_DATA)
os.environ["DATABASE_URL"] = f"sqlite:///{(_TEST_RUNTIME_DATA / 'bootstrap.db').as_posix()}"
atexit.register(shutil.rmtree, _TEST_RUNTIME_DATA, True)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database import create_database_engine, get_db
from app.dependencies import get_tutor_provider
import app.services.startup as startup_module
import app.routers.tutor_routes.settings as tutor_settings_router_module
from app.main import app
from app.tutor import CodexConnectionStatus, TutorContext


class TestTutorProvider:
    """Offline default for endpoints that exercise the dialogue flow in tests."""

    def respond(self, context: TutorContext) -> str:
        prompt = context.prompt.lower()
        if "домашнее задание" in prompt:
            return (
                '{"title":"Тестовое домашнее задание","description":"Выполни одно тестовое задание.",'
                '"focus_category":"test"}'
            )
        if "только json" in prompt:
            return (
                '{"is_correct":true,"score":100,"corrected_answer":"Тестовый ответ",'
                '"explanation":"Тестовая проверка.","next_exercise":"Продолжай.",'
                '"mistake_category":null,"new_words":[]}'
            )
        return "Тестовый ответ преподавателя."


@pytest.fixture
def client(tmp_path: Path) -> Generator[TestClient, None, None]:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    test_engine = create_database_engine(database_url)
    test_session = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

    def override_get_db() -> Generator[Session, None, None]:
        db = test_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tutor_provider] = lambda: TestTutorProvider()
    settings = get_settings()
    original_database_url = settings.database_url
    original_learning_path = settings.learning_path
    original_project_root = settings.project_root
    original_tutor_values = (
        settings.tutor_provider,
        settings.openai_api_key,
        settings.openai_model,
        settings.polza_api_key,
        settings.polza_model,
    )
    original_engine = startup_module.engine
    original_codex_status = tutor_settings_router_module.get_codex_connection_status
    tutor_settings_router_module.get_codex_connection_status = lambda _: CodexConnectionStatus(True, True, "Codex подключён в тесте")
    settings.database_url = database_url
    settings.learning_path = Path(__file__).parents[2] / "course-content" / "slovak-a1" / "learning"
    settings.project_root = tmp_path
    startup_module.engine = test_engine
    with TestClient(app) as test_client:
        yield test_client
    settings.database_url = original_database_url
    settings.learning_path = original_learning_path
    settings.project_root = original_project_root
    (
        settings.tutor_provider,
        settings.openai_api_key,
        settings.openai_model,
        settings.polza_api_key,
        settings.polza_model,
    ) = original_tutor_values
    startup_module.engine = original_engine
    tutor_settings_router_module.get_codex_connection_status = original_codex_status
    app.dependency_overrides.clear()
    test_engine.dispose()
