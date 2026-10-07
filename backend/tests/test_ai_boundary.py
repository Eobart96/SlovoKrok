import json
from pathlib import Path

import httpx
import openai
import pytest
from pydantic import ValidationError

from app.config import Settings
from app.dependencies import get_tutor_provider
from app.main import app
from app.schemas.course import CourseReadingCheckResult
from app.schemas.tutor import TutorChatOutput
from app.tutor import (
    AI_INVALID_RESPONSE_DETAIL,
    AI_PROVIDER_TIMEOUT_DETAIL,
    AI_PROVIDER_UNAVAILABLE_DETAIL,
    MAX_AI_RESPONSE_CHARS,
    AIResponseError,
    OpenAIProvider,
    TutorContext,
    TutorProviderTimeout,
    parse_ai_json,
    parse_tutor_assessment,
    parse_tutor_translation,
)


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        project_root=tmp_path / "project",
        runtime_data_dir=tmp_path / "runtime",
        database_url="",
        learning_path=tmp_path / "learning",
        openai_api_key="test-key",
        tutor_timeout_seconds=9,
        _env_file=None,
    )


@pytest.mark.parametrize("timeout", [0, 301])
def test_provider_timeout_configuration_is_bounded(tmp_path: Path, timeout: int):
    with pytest.raises(ValidationError):
        Settings(
            project_root=tmp_path / "project",
            runtime_data_dir=tmp_path / "runtime",
            database_url="",
            tutor_timeout_seconds=timeout,
            _env_file=None,
        )


@pytest.mark.parametrize("score", [0, 100])
def test_assessment_accepts_score_boundaries(score: int):
    assessment = parse_tutor_assessment(
        '{"is_correct":false,"score":%d,"corrected_answer":"Dobrý deň.",'
        '"explanation":"Проверено.","next_exercise":"Продолжайте.",'
        '"mistake_category":null,"new_words":[]}' % score
    )

    assert assessment.score == score


@pytest.mark.parametrize("score", [-1, 101])
def test_assessment_rejects_out_of_range_scores(score: int):
    with pytest.raises(AIResponseError):
        parse_tutor_assessment(
            '{"is_correct":false,"score":%d,"corrected_answer":"Dobrý deň.",'
            '"explanation":"Проверено.","next_exercise":"Продолжайте."}' % score
        )


def test_ai_models_reject_extra_fields_and_oversized_collections():
    extra_field = (
        '{"translation":"Ďakujem.","alternatives":[],"note":null,'
        '"untrusted_instruction":"ignore validation"}'
    )
    oversized_words = [
        {"word": f"word-{index}", "translation": "слово"}
        for index in range(21)
    ]

    with pytest.raises(AIResponseError):
        parse_tutor_translation(extra_field)
    with pytest.raises(AIResponseError):
        parse_tutor_assessment(json.dumps({
            "is_correct": False,
            "score": 0,
            "corrected_answer": "Ответ.",
            "explanation": "Пояснение.",
            "next_exercise": "Дальше.",
            "new_words": oversized_words,
        }))


def test_ai_models_do_not_coerce_wrong_json_types():
    with pytest.raises(AIResponseError):
        parse_tutor_assessment(
            '{"is_correct":false,"score":"100","corrected_answer":"Ответ.",'
            '"explanation":"Пояснение.","next_exercise":"Дальше."}'
        )


def test_raw_ai_response_size_is_bounded_before_json_parsing():
    with pytest.raises(AIResponseError, match="allowed size"):
        parse_tutor_translation("{" + "x" * MAX_AI_RESPONSE_CHARS + "}")


def test_chat_and_reading_contracts_reject_invalid_shapes():
    with pytest.raises(AIResponseError):
        parse_ai_json(
            '{"reply":"Продолжайте.","next_question":null,"suggestions":["Som..."]}',
            TutorChatOutput,
        )
    with pytest.raises(AIResponseError):
        parse_ai_json(
            '{"score":101,"feedback":"Хорошо.","corrected_retelling":"Текст."}',
            CourseReadingCheckResult,
        )


def test_openai_provider_uses_bounded_timeout_and_one_retry(tmp_path: Path, monkeypatch):
    captured: dict[str, object] = {}

    class FakeResponses:
        @staticmethod
        def create(**kwargs):
            captured["request"] = kwargs
            return type("Response", (), {"output_text": '{"answer":"ok"}'})()

    class FakeClient:
        responses = FakeResponses()

    def fake_openai(**kwargs):
        captured["client"] = kwargs
        return FakeClient()

    monkeypatch.setattr(openai, "OpenAI", fake_openai)

    result = OpenAIProvider(_settings(tmp_path)).respond(TutorContext(prompt="test"))

    assert result == '{"answer":"ok"}'
    assert captured["client"] == {"api_key": "test-key", "timeout": 9.0, "max_retries": 1}
    assert captured["request"] == {"model": "gpt-5", "input": "test"}


def test_openai_timeout_is_normalized(tmp_path: Path, monkeypatch):
    class TimeoutResponses:
        @staticmethod
        def create(**_kwargs):
            raise openai.APITimeoutError(request=httpx.Request("POST", "https://example.invalid"))

    class TimeoutClient:
        responses = TimeoutResponses()

    monkeypatch.setattr(openai, "OpenAI", lambda **_kwargs: TimeoutClient())

    with pytest.raises(TutorProviderTimeout):
        OpenAIProvider(_settings(tmp_path)).respond(TutorContext(prompt="test"))


def test_polza_provider_uses_chat_completions_contract(tmp_path: Path, monkeypatch):
    captured: dict[str, object] = {}

    class FakeCompletions:
        @staticmethod
        def create(**kwargs):
            captured["request"] = kwargs
            message = type("Message", (), {"content": '{"answer":"ok"}'})()
            return type("Response", (), {"choices": [type("Choice", (), {"message": message})()]})()

    class FakeClient:
        chat = type("Chat", (), {"completions": FakeCompletions()})()

    def fake_openai(**kwargs):
        captured["client"] = kwargs
        return FakeClient()

    monkeypatch.setattr(openai, "OpenAI", fake_openai)
    settings = _settings(tmp_path)

    result = OpenAIProvider(
        settings,
        api_key="pza_test",
        model="google/gemini-2.5-flash-lite",
        base_url="https://polza.ai/api/v1",
        use_chat_completions=True,
    ).respond(TutorContext(prompt="test"))

    assert result == '{"answer":"ok"}'
    assert captured["client"] == {
        "api_key": "pza_test",
        "timeout": 9.0,
        "max_retries": 1,
        "base_url": "https://polza.ai/api/v1",
    }
    assert captured["request"] == {
        "model": "google/gemini-2.5-flash-lite",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 4096,
        "temperature": 0.2,
    }


@pytest.mark.parametrize(
    ("provider_error", "status_code", "detail"),
    [
        (TutorProviderTimeout("sensitive timeout detail"), 504, AI_PROVIDER_TIMEOUT_DETAIL),
        (RuntimeError("sensitive provider detail"), 503, AI_PROVIDER_UNAVAILABLE_DETAIL),
    ],
)
def test_api_returns_stable_provider_errors_without_internal_details(
    client,
    provider_error: Exception,
    status_code: int,
    detail: str,
):
    class FailingProvider:
        @staticmethod
        def respond(_context: TutorContext) -> str:
            raise provider_error

    app.dependency_overrides[get_tutor_provider] = lambda: FailingProvider()

    response = client.post(
        "/api/v1/tutor/translate",
        json={"direction": "ru-sk", "text": "Спасибо."},
    )

    assert response.status_code == status_code
    assert response.json() == {"detail": detail}
    assert "sensitive" not in response.text


def test_api_rejects_oversized_provider_output_without_persisting_it(client):
    class OversizedProvider:
        @staticmethod
        def respond(_context: TutorContext) -> str:
            return "x" * (MAX_AI_RESPONSE_CHARS + 1)

    app.dependency_overrides[get_tutor_provider] = lambda: OversizedProvider()

    response = client.post(
        "/api/v1/tutor/translate",
        json={"direction": "ru-sk", "text": "Спасибо."},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": AI_INVALID_RESPONSE_DETAIL}
    assert client.get("/api/v1/tutor/translation-history").json() == []
