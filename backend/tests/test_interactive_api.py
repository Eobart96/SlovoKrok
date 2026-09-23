from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from app.config import Settings
from app.database import get_db
from app.dependencies import get_tutor_provider
from app.main import app
from app.models import CourseExercise, CourseExerciseAttempt
import app.services.startup as startup_module
from app.tutor import TutorContext, build_reading_generation_context, build_tutor_context, encode_exercise_snapshot, parse_generated_exercise


class InteractiveTutorProvider:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def respond(self, context: TutorContext) -> str:
        self.prompts.append(context.prompt)
        prompt = context.prompt.lower()
        if "помощник по переводу" in prompt:
            return '{"answer":"Ďakujem — нейтральное «спасибо», а Vďaka звучит разговорнее."}'
        if "профессиональный переводчик" in prompt:
            if "на словацкий" in prompt:
                return '{"translation":"Ďakujem.","alternatives":["Vďaka."],"note":"Ďakujem — нейтральная форма благодарности."}'
            return '{"translation":"Спасибо.","alternatives":[],"note":null}'
        if "проведи один короткий шаг" in prompt:
            return (
                '{"reply":"Dobre, pokračujeme.","correction":null,'
                '"explanation":null,"next_question":"Ako sa voláte?",'
                '"suggestions":["Volám sa…","Ja som…"],'
                '"mistake_original":null,"mistake_corrected":null}'
            )
        if "генератор упражнений" in prompt:
            return (
                '{"question":"Соедините приветствия с переводами.",'
                '"instruction":"Выберите пару для каждой фразы.","interaction_type":"match",'
                '"pairs":[{"prompt":"Dobrý deň","answer":"Здравствуйте"},'
                '{"prompt":"Dovidenia","answer":"До свидания"}]}'
            )
        if "составь короткий текст для чтения" in prompt:
            return (
                '{"title":"Приветствие","text":"Dobrý deň. Volám sa Anna. Teší ma.",'
                '"instruction":"Прочитай и перескажи текст."}'
            )
        if "проверь пересказ" in prompt:
            return '{"score":90,"feedback":"Содержание понято.","corrected_retelling":"Анна представилась."}'
        if "создай одно небольшое домашнее задание" in prompt:
            return (
                '{"title":"Представьтесь","description":"Напишите две фразы о себе.",'
                '"focus_category":"introductions"}'
            )
        if "проверь ответ" in prompt or "проверь домашнее задание" in prompt:
            return (
                '{"is_correct":true,"score":100,"corrected_answer":"Dobrý deň",'
                '"explanation":"Ответ принят.","next_exercise":"Продолжайте.",'
                '"mistake_category":null,"new_words":[]}'
            )
        raise AssertionError(f"Unexpected tutor prompt: {context.prompt[:120]}")


def _state_payload() -> dict[str, object]:
    return {
        "activeModule": 1,
        "selectedSlug": "greetings",
        "fontSize": "large",
        "progress": {"greetings": "in_progress"},
        "lessonSteps": {},
        "checkSelections": {},
        "practiceAnswers": {},
        "practiceResults": {},
        "mistakes": {},
        "finalSelections": {},
        "finalCompleted": False,
        "finalCompletedModules": {},
        "chatHistories": {},
        "lessonSummaries": {},
        "personalCheatSheets": [],
    }


def _state_headers(revision: str | None) -> dict[str, str]:
    return {"X-Course-State-Revision": revision or "none"}


def test_only_interactive_runtime_routes_are_exposed(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/ui/").status_code == 404
    assert client.get("/api/v1/courses").status_code == 404
    assert client.get("/api/v1/progress").status_code == 404
    assert client.get("/api/v1/tutor/settings").status_code == 200
    assert client.get("/api/v1/course/state").status_code == 200


def test_tutor_settings_save_provider_without_exposing_key(client):
    secret = "test-openai-key-never-return"
    response = client.put(
        "/api/v1/tutor/settings",
        json={"provider": "openai", "openai_api_key": secret, "openai_model": "gpt-5", "polza_model": "openai/gpt-4o-mini"},
    )

    assert response.status_code == 200
    assert response.json()["provider"] == "openai"
    assert response.json()["openai_api_key_configured"] is True
    assert secret not in response.text
    restored = client.get("/api/v1/tutor/settings")
    assert secret not in restored.text


def test_tutor_settings_require_key_and_allow_switching_back_to_codex(client):
    missing = client.put(
        "/api/v1/tutor/settings",
        json={"provider": "polza", "openai_model": "gpt-5", "polza_model": "openai/gpt-4o-mini"},
    )
    assert missing.status_code == 422
    assert "API-ключ" in missing.json()["detail"]

    codex = client.put(
        "/api/v1/tutor/settings",
        json={"provider": "codex", "openai_model": "gpt-5", "polza_model": "openai/gpt-4o-mini"},
    )
    assert codex.status_code == 200
    assert codex.json()["provider"] == "codex"


def test_course_state_round_trip_and_legacy_defaults(client):
    assert client.get("/api/v1/course/state").json()["exists"] is False

    payload = _state_payload()
    payload["personalCheatSheets"] = [{
        "id": "note-1", "title": "Моё правило", "content": "После do — Genitív.",
        "createdAt": "2026-09-13T12:00:00Z", "updatedAt": "2026-09-13T12:00:00Z",
    }]
    saved = client.put("/api/v1/course/state", json=payload, headers=_state_headers(None))
    assert saved.status_code == 200
    assert saved.json()["schema_version"] == 2
    assert len(saved.json()["revision"]) == 64
    assert saved.json()["state"]["selectedSlug"] == "greetings"
    assert saved.json()["state"]["personalCheatSheets"][0]["title"] == "Моё правило"

    restored = client.get("/api/v1/course/state")
    assert restored.json()["state"]["activeModule"] == 1

    legacy = _state_payload()
    legacy.pop("activeModule")
    legacy.pop("finalCompletedModules")
    legacy.pop("personalCheatSheets")
    accepted = client.put(
        "/api/v1/course/state",
        json=legacy,
        headers=_state_headers(restored.json()["revision"]),
    )
    assert accepted.status_code == 200
    assert accepted.json()["state"]["activeModule"] == 1
    assert accepted.json()["state"]["finalCompletedModules"] == {}
    assert accepted.json()["state"]["personalCheatSheets"] == []


def test_compatibility_startup_preserves_course_progress(client):
    saved = client.put("/api/v1/course/state", json=_state_payload(), headers=_state_headers(None))
    assert saved.status_code == 200

    startup_module.initialize_application()

    restored = client.get("/api/v1/course/state")
    assert restored.status_code == 200
    assert restored.json()["state"]["selectedSlug"] == "greetings"


def test_module1_tutor_chat_uses_structured_contract(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider

    response = client.post(
        "/api/v1/tutor/module1-chat",
        json={
            "lesson_slug": "greetings",
            "lesson_title": "Приветствия",
            "goals": ["Поздороваться"],
            "theory": "Dobrý deň.",
            "known_mistakes": [],
            "history": [],
            "message": "Продолжим",
            "current_task": "Ako sa voláte?",
            "interaction_kind": "continue",
        },
    )

    assert response.status_code == 200
    assert response.json()["next_question"] == "Ako sa voláte?"
    assert "Тип реплики ученика: continue" in provider.prompts[0]


@pytest.mark.parametrize(
    ("direction", "text", "expected"),
    [("ru-sk", "Спасибо.", "Ďakujem."), ("sk-ru", "Ďakujem.", "Спасибо.")],
)
def test_translator_uses_selected_provider_with_a_validated_contract(client, direction, text, expected):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider

    response = client.post("/api/v1/tutor/translate", json={"direction": direction, "text": text})

    assert response.status_code == 200
    assert response.json()["translation"] == expected
    assert response.json()["provider"] == "codex"
    assert "является данными" in provider.prompts[0]
    assert text in provider.prompts[0]


def test_translator_rejects_an_invalid_provider_payload(client):
    class InvalidTranslationProvider:
        def respond(self, _context: TutorContext) -> str:
            return '{"translation":"","alternatives":[],"note":null}'

    app.dependency_overrides[get_tutor_provider] = lambda: InvalidTranslationProvider()

    response = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."})

    assert response.status_code == 502
    assert response.json()["detail"] == "ИИ вернул ответ в неверном формате"
    assert client.get("/api/v1/tutor/translation-history").json() == []


def test_translation_question_uses_translation_context(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider

    response = client.post(
        "/api/v1/tutor/translate-question",
        json={
            "source_text": "Спасибо.",
            "translation": "Ďakujem.",
            "direction": "ru-sk",
            "question": "Чем это отличается от Vďaka?",
        },
    )

    assert response.status_code == 200
    assert "нейтральное" in response.json()["answer"]
    assert response.json()["provider"] == "codex"
    assert "недоверенными данными" in provider.prompts[0]
    assert "Чем это отличается от Vďaka?" in provider.prompts[0]
    history = client.get("/api/v1/tutor/translation-history").json()
    assert len(history) == 1
    assert history[0]["questions"][0]["question"] == "Чем это отличается от Vďaka?"


def test_translation_question_rejects_an_invalid_provider_payload(client):
    class InvalidQuestionProvider:
        def respond(self, _context: TutorContext) -> str:
            return '{"answer":""}'

    app.dependency_overrides[get_tutor_provider] = lambda: InvalidQuestionProvider()
    response = client.post(
        "/api/v1/tutor/translate-question",
        json={"source_text": "Спасибо.", "translation": "Ďakujem.", "direction": "ru-sk", "question": "Почему?"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "ИИ вернул ответ в неверном формате"


def test_translator_history_autosaves_and_lists(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider

    translated = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."})
    newer = client.post("/api/v1/tutor/translate", json={"direction": "sk-ru", "text": "Dobrý deň."})

    assert translated.status_code == 200
    assert newer.status_code == 200
    assert translated.json()["history_id"] > 0
    newest_page = client.get("/api/v1/tutor/translation-history?limit=1").json()
    assert [item["id"] for item in newest_page] == [newer.json()["history_id"]]
    older_page = client.get(
        f"/api/v1/tutor/translation-history?limit=1&before_id={newer.json()['history_id']}"
    ).json()
    assert [item["id"] for item in older_page] == [translated.json()["history_id"]]
    assert older_page[0]["source_text"] == "Спасибо."
    assert older_page[0]["translation"] == "Ďakujem."
    assert older_page[0]["alternatives"] == ["Vďaka."]
    assert older_page[0]["questions"] == []


def test_translator_history_links_questions_to_saved_translation(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    translated = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."}).json()

    answered = client.post(
        "/api/v1/tutor/translate-question",
        json={
            "history_id": translated["history_id"],
            "source_text": "этот текст не должен заменить сохранённый",
            "translation": "неверный контекст",
            "direction": "sk-ru",
            "question": "Чем это отличается от Vďaka?",
        },
    )

    assert answered.status_code == 200
    assert answered.json()["history_id"] == translated["history_id"]
    assert "Спасибо." in provider.prompts[-1]
    assert "неверный контекст" not in provider.prompts[-1]
    history = client.get("/api/v1/tutor/translation-history").json()
    assert history[0]["questions"][0]["question"] == "Чем это отличается от Vďaka?"
    assert "нейтральное" in history[0]["questions"][0]["answer"]


def test_translator_history_deletes_one_entry_with_its_questions(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    translated = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."}).json()
    client.post(
        "/api/v1/tutor/translate-question",
        json={
            "history_id": translated["history_id"],
            "source_text": "Спасибо.",
            "translation": "Ďakujem.",
            "direction": "ru-sk",
            "question": "Почему?",
        },
    ).raise_for_status()

    deleted = client.delete(f"/api/v1/tutor/translation-history/{translated['history_id']}")

    assert deleted.json() == {"deleted": True}
    assert client.get("/api/v1/tutor/translation-history").json() == []
    assert client.delete(f"/api/v1/tutor/translation-history/{translated['history_id']}").status_code == 404


def test_translator_history_clear_requires_confirmation_and_removes_all(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    first = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."}).json()
    client.post("/api/v1/tutor/translate", json={"direction": "sk-ru", "text": "Ďakujem."}).raise_for_status()
    client.post(
        "/api/v1/tutor/translate-question",
        json={
            "history_id": first["history_id"],
            "source_text": "Спасибо.",
            "translation": "Ďakujem.",
            "direction": "ru-sk",
            "question": "Почему?",
        },
    ).raise_for_status()

    assert client.request("DELETE", "/api/v1/tutor/translation-history", json={}).status_code == 422
    cleared = client.request(
        "DELETE",
        "/api/v1/tutor/translation-history",
        json={"confirmation": "delete-translation-history"},
    )

    assert cleared.json() == {"deleted": True, "translations_deleted": 2, "questions_deleted": 1}
    assert client.get("/api/v1/tutor/translation-history").json() == []


def test_translator_history_rolls_back_when_database_commit_fails(client, monkeypatch):
    from sqlalchemy.exc import OperationalError
    from sqlalchemy.orm import Session

    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    original_commit = Session.commit

    def fail_commit(_session):
        raise OperationalError("INSERT", {}, RuntimeError("test commit failure"))

    monkeypatch.setattr(Session, "commit", fail_commit)
    response = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."})
    monkeypatch.setattr(Session, "commit", original_commit)

    assert response.status_code == 503
    assert response.json()["detail"] == "Не удалось сохранить перевод в локальной истории"
    assert client.get("/api/v1/tutor/translation-history").json() == []


def test_module1_exercise_lifecycle(client):
    provider = InteractiveTutorProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    created = client.post(
        "/api/v1/course/exercises",
        json={"lesson_slug": "greetings", "lesson_title": "Приветствия", "theory": "Формат нового упражнения: Соедини пары.\nТип интерактива: match.\nDobrý deň."},
    )
    assert created.status_code == 200
    assert "Формат нового упражнения: Соедини пары." in provider.prompts[0]
    assert "строго сохрани их" in provider.prompts[0]
    assert "один короткий ответ ученика" in provider.prompts[0]
    assert created.json()["interaction_type"] == "match"
    assert created.json()["pair_prompts"] == ["Dobrý deň", "Dovidenia"]
    assert created.json()["pair_options"] == ["До свидания", "Здравствуйте"]
    assert list(zip(created.json()["pair_prompts"], created.json()["pair_options"])) != [("Dobrý deň", "Здравствуйте"), ("Dovidenia", "До свидания")]
    exercise_id = created.json()["id"]

    checked = client.post(
        f"/api/v1/course/exercises/{exercise_id}/answer",
        json={"answer": "Dobrý deň"},
    )
    assert checked.status_code == 200
    assert checked.json()["is_correct"] is True
    assert '"answer":"Здравствуйте"' in provider.prompts[1]
    listed = client.get("/api/v1/course/exercises?lesson_slug=greetings").json()[0]
    assert listed["interaction_type"] == "match"
    assert listed["latest_attempt"] is not None
    assert client.delete(f"/api/v1/course/exercises/{exercise_id}").json() == {"deleted": True}


def test_legacy_exercise_without_interaction_metadata_remains_readable(client):
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        legacy = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question="Переведите приветствие", instruction="Введите ответ.", theory_snapshot="Dobrý deň.")
        db.add(legacy)
        db.commit()
    finally:
        database_provider.close()
    response = client.get("/api/v1/course/exercises?lesson_slug=greetings")
    assert response.status_code == 200
    assert response.json()[0]["interaction_type"] == "text"
    assert response.json()[0]["options"] == []
    assert response.json()[0]["pair_prompts"] == []


def test_saved_correct_exercise_attempt_with_low_score_is_returned_as_100(client):
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        exercise = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question="Переведите", instruction="Введите ответ.", theory_snapshot="Dobrý deň.")
        db.add(exercise)
        db.flush()
        db.add(CourseExerciseAttempt(exercise_id=exercise.id, answer="Dobrý deň", is_correct=True, score=1, corrected_answer="Dobrý deň", explanation="Правильно.", next_exercise="Продолжайте."))
        db.commit()
    finally:
        database_provider.close()

    response = client.get("/api/v1/course/exercises?lesson_slug=greetings")
    assert response.status_code == 200
    assert response.json()[0]["latest_attempt"]["is_correct"] is True
    assert response.json()[0]["latest_attempt"]["score"] == 100


def test_delete_all_exercises_requires_confirmation_and_removes_attempts(client):
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        first = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question="Первое", instruction="Ответьте.", theory_snapshot="Dobrý deň.")
        second = CourseExercise(lesson_slug="numbers", lesson_title="Числа", question="Второе", instruction="Ответьте.", theory_snapshot="jeden.")
        db.add_all([first, second])
        db.flush()
        db.add(CourseExerciseAttempt(exercise_id=first.id, answer="Dobrý deň", is_correct=True, score=100, corrected_answer="Dobrý deň", explanation="Верно.", next_exercise="Продолжайте."))
        db.commit()
    finally:
        database_provider.close()

    rejected = client.request("DELETE", "/api/v1/course/exercises", json={"confirmation": "wrong"})
    assert rejected.status_code == 422
    assert len(client.get("/api/v1/course/exercises").json()) == 2

    deleted = client.request("DELETE", "/api/v1/course/exercises", json={"confirmation": "delete-all-exercises"})
    assert deleted.status_code == 200
    assert deleted.json() == {"deleted": True, "exercises_deleted": 2, "attempts_deleted": 1}
    assert client.get("/api/v1/course/exercises").json() == []

    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        assert db.query(CourseExerciseAttempt).count() == 0
    finally:
        database_provider.close()


@pytest.mark.parametrize(
    ("payload", "answer"),
    [
        ('{"question":"Выберите приветствие.","instruction":"Нажмите вариант.","interaction_type":"choice","options":["Ahoj","Dobrý deň"],"accepted_answers":["Dobrý deň"]}', "  dobrý   DEŇ "),
        ('{"question":"Соберите фразу.","instruction":"Нажмите слова.","interaction_type":"order","tokens":["deň","Dobrý"],"accepted_answers":["Dobrý deň"]}', "Dobrý deň"),
        ('{"question":"Соедините пары.","instruction":"Выберите пары.","interaction_type":"match","pairs":[{"prompt":"Dobrý deň","answer":"Здравствуйте"},{"prompt":"Dovidenia","answer":"До свидания"}]}', "Dobrý deň → Здравствуйте; Dovidenia → До свидания"),
        ('{"question":"Переведите.","instruction":"Введите ответ.","interaction_type":"text","accepted_answers":["Dovidenia","Do videnia"]}', "dovidenia"),
    ],
)
def test_offline_exercise_uses_saved_reference_without_provider(client, payload, answer):
    class ProviderMustNotRun:
        def respond(self, context: TutorContext) -> str:
            raise AssertionError("Offline assessment called the AI provider")

    app.dependency_overrides[get_tutor_provider] = ProviderMustNotRun
    generated = parse_generated_exercise(payload)
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        exercise = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question=generated.question, instruction=generated.instruction, theory_snapshot=encode_exercise_snapshot("Dobrý deň.", generated))
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        exercise_id = exercise.id
    finally:
        database_provider.close()

    checked = client.post(
        f"/api/v1/course/exercises/{exercise_id}/answer",
        json={"answer": answer, "assessment_mode": "offline"},
    )
    assert checked.status_code == 200
    assert checked.json()["is_correct"] is True
    assert checked.json()["score"] == 100
    assert "сохранённым эталоном" in checked.json()["explanation"]


def test_offline_exercise_rejects_legacy_without_reference(client):
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        legacy = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question="Переведите", instruction="Введите ответ.", theory_snapshot="Dobrý deň.")
        db.add(legacy)
        db.commit()
        db.refresh(legacy)
        exercise_id = legacy.id
    finally:
        database_provider.close()

    checked = client.post(
        f"/api/v1/course/exercises/{exercise_id}/answer",
        json={"answer": "Dobrý deň", "assessment_mode": "offline"},
    )
    assert checked.status_code == 409
    assert "онлайн-режим" in checked.json()["detail"]


def test_module1_reading_lifecycle(client):
    app.dependency_overrides[get_tutor_provider] = InteractiveTutorProvider
    created = client.post(
        "/api/v1/course/readings",
        json={
            "lesson_slug": "greetings",
            "lesson_title": "Приветствия",
            "theory": "Dobrý deň.",
            "completed_theory": "",
        },
    )
    assert created.status_code == 200
    reading_id = created.json()["id"]

    checked = client.post(
        f"/api/v1/course/readings/{reading_id}/check",
        json={"retelling": "Анна представилась."},
    )
    assert checked.status_code == 200
    assert checked.json()["score"] == 90
    assert client.get("/api/v1/course/readings").json()[0]["latest_attempt"] is not None
    assert client.delete(f"/api/v1/course/readings/{reading_id}").json() == {"deleted": True}


def test_reading_generation_prompt_uses_unlocked_vocabulary_without_future_grammar():
    context = build_reading_generation_context(
        lesson_title="Приветствия",
        theory="Только настоящее время и изученные модели.",
        completed_theory="Dobrý deň = Добрый день\nrodina = семья",
    )
    assert "Открытые слова и фразы ученика" in context.prompt
    assert "не менее 8 его элементов" in context.prompt
    assert "не разрешает будущую грамматику" in context.prompt
    assert "Не вводи новые смысловые слова вне открытого списка" in context.prompt
    assert "Dobrý deň = Добрый день" in context.prompt


def test_module1_vocabulary_sync_and_review(client):
    payload = {
        "items": [
            {
                "lesson_slug": "greetings",
                "lesson_title": "Приветствия",
                "word": "Dobrý deň",
                "translation": "Добрый день",
                "example": "Dobrý deň, Anna.",
            }
        ]
    }
    synced = client.put("/api/v1/course/vocabulary/sync", json=payload)
    assert synced.status_code == 200
    item_id = synced.json()[0]["id"]

    repeated = client.put("/api/v1/course/vocabulary/sync", json=payload)
    assert repeated.status_code == 200
    assert [item["id"] for item in repeated.json()] == [item_id]

    with ThreadPoolExecutor(max_workers=2) as executor:
        responses = list(
            executor.map(
                lambda _: client.put("/api/v1/course/vocabulary/sync", json=payload),
                range(2),
            )
        )
    assert [response.status_code for response in responses] == [200, 200]
    assert all([item["id"] for item in response.json()] == [item_id] for response in responses)

    reviewed = client.post(f"/api/v1/course/vocabulary/{item_id}/review")
    assert reviewed.status_code == 200
    assert reviewed.json()["review_count"] == 1
    assert reviewed.json()["interval_days"] == 1

    resynced_after_review = client.put("/api/v1/course/vocabulary/sync", json=payload)
    assert resynced_after_review.status_code == 200
    assert resynced_after_review.json()[0]["review_count"] == 1
    assert resynced_after_review.json()[0]["interval_days"] == 1


def test_module1_homework_lifecycle(client):
    app.dependency_overrides[get_tutor_provider] = InteractiveTutorProvider
    created = client.post(
        "/api/v1/course/homework",
        json={
            "lesson_slug": "introductions",
            "lesson_title": "Представление",
            "theory": "Volám sa…",
            "known_mistakes": [],
        },
    )
    assert created.status_code == 200
    homework_id = created.json()["id"]

    submitted = client.post(
        f"/api/v1/course/homework/{homework_id}/submit",
        json={"answer": "Volám sa Anna."},
    )
    assert submitted.status_code == 200
    assert submitted.json()["is_correct"] is True
    assert client.get("/api/v1/course/homework").json()[0]["latest_attempt"] is not None
    assert client.delete(f"/api/v1/course/homework/{homework_id}").json() == {"deleted": True}


def test_tutor_context_does_not_share_private_profile_by_default(tmp_path: Path):
    project_root = Path(__file__).parents[2]
    local_profile = tmp_path / ".ai" / "private" / "student_profile.local.md"
    local_profile.parent.mkdir(parents=True)
    local_profile.write_text("Локальная настройка ученика.", encoding="utf-8")
    settings = Settings(
        project_root=tmp_path,
        learning_path=project_root / "course-content" / "slovak-a1" / "learning",
    )

    context = build_tutor_context(settings, "Начнём урок")

    assert "Локальная настройка ученика." not in context.prompt
    assert "Это публичный пример профиля" in context.prompt
