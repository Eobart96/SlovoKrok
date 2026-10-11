import json

import pytest
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_tutor_provider
from app.main import app
from app.models import CourseHomework, CourseHomeworkAttempt


class QuestionProvider:
    def __init__(self, response='{"answer":"Obed мужского рода, поэтому используем ho — его."}'):
        self.response = response
        self.contexts = []

    def respond(self, context):
        self.contexts.append(context)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def seed_review(slug="a2-m4-aspect"):
    dependency = app.dependency_overrides[get_db]()
    db = next(dependency)
    try:
        homework = CourseHomework(lesson_slug=slug, lesson_title="Вид глагола", title="Обед", description="Напишите о приготовлении обеда.", focus_category="pronouns", theory_snapshot="Obed — мужской род.")
        db.add(homework)
        db.flush()
        attempt = CourseHomeworkAttempt(homework_id=homework.id, answer="Uvarím jo.", corrected_answer="Uvarím ho.", explanation="Obed мужского рода.", next_exercise="Повторите местоимение.", score=90, is_correct=False)
        db.add(attempt)
        db.commit()
        return homework.id, attempt.id
    finally:
        dependency.close()


def test_question_uses_saved_attempt_and_does_not_write_or_change_score(client, monkeypatch):
    homework_id, attempt_id = seed_review()
    provider = QuestionProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    before = client.get("/api/v1/course/homework").json()
    state = client.get("/api/v1/course/state").json()

    def forbid_commit(_db):
        raise AssertionError("Asking must not write to SQLite")

    monkeypatch.setattr(Session, "commit", forbid_commit)
    response = client.post(f"/api/v1/course/homework/{homework_id}/question", json={"attempt_id": attempt_id, "question": "Почему ho?"})
    assert response.status_code == 200
    assert response.json()["answer"].startswith("Obed")
    prompt = provider.contexts[0].prompt
    for text in ("словацкому A2", "Uvarím jo.", "Uvarím ho.", "Obed мужского рода.", "Почему ho?", "Напишите о приготовлении обеда."):
        assert text in prompt
    assert provider.contexts[0].response_schema["required"] == ["answer"]
    assert client.get("/api/v1/course/homework").json() == before
    assert client.get("/api/v1/course/state").json() == state


def test_question_rejects_missing_or_other_homework_attempt_before_provider(client):
    homework_id, attempt_id = seed_review()
    other_id, other_attempt_id = seed_review("greetings")
    provider = QuestionProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    for task_id, review_id in ((homework_id, other_attempt_id), (homework_id, 999999), (999999, attempt_id)):
        response = client.post(f"/api/v1/course/homework/{task_id}/question", json={"attempt_id": review_id, "question": "Почему?"})
        assert response.status_code == 404
    assert other_id != homework_id
    assert provider.contexts == []


@pytest.mark.parametrize("question", ["", "   ", "a" * 2001])
def test_question_bounds(client, question):
    homework_id, attempt_id = seed_review()
    assert client.post(f"/api/v1/course/homework/{homework_id}/question", json={"attempt_id": attempt_id, "question": question}).status_code == 422


@pytest.mark.parametrize("output,status", [("{}", 502), (json.dumps({"answer": " "}), 502), (RuntimeError("offline"), 503)])
def test_question_provider_failures_keep_saved_review(client, output, status):
    homework_id, attempt_id = seed_review("greetings")
    before = client.get("/api/v1/course/homework").json()
    app.dependency_overrides[get_tutor_provider] = lambda: QuestionProvider(output)
    response = client.post(f"/api/v1/course/homework/{homework_id}/question", json={"attempt_id": attempt_id, "question": "Почему?"})
    assert response.status_code == status
    assert client.get("/api/v1/course/homework").json() == before
