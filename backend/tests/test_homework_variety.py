import json

import pytest

from app.dependencies import ProfileTutorProvider, get_tutor_provider
from app.main import app
from app.services import learner_profile


class HomeworkProvider:
    def __init__(self, descriptions):
        self.descriptions = iter(descriptions)
        self.prompts = []

    def respond(self, context):
        self.prompts.append(context.prompt)
        return json.dumps({"title": "Практика", "description": next(self.descriptions), "focus_category": "Знакомство", "reference_answer": "Volám sa Anna."})


def generate(client, slug="greetings", **batch):
    return client.post("/api/v1/course/homework", json={"lesson_slug": slug, "lesson_title": "Знакомство", "theory": "Настоящее время. Короткие реплики.", **batch})


@pytest.fixture(autouse=True)
def isolated_profile(monkeypatch):
    monkeypatch.setattr(learner_profile, "read_profile", lambda: learner_profile.LearnerProfile())


def test_homework_history_and_format_include_earlier_items_of_the_same_batch_only(client, monkeypatch):
    monkeypatch.setattr(learner_profile, "read_profile", lambda: learner_profile.LearnerProfile(share_with_ai=True))
    provider = HomeworkProvider(["Представьтесь соседу.", "Не повторяйте этот текст A2.", "Уточните имя собеседника."])
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    assert generate(client, batch_index=1, batch_total=2).status_code == 200
    assert generate(client, "a2-intro").status_code == 200
    assert generate(client, batch_index=2, batch_total=2).status_code == 200
    assert "Представьтесь соседу." in provider.prompts[-1]
    assert "Не повторяйте этот текст A2." not in provider.prompts[-1]
    assert "Мини-диалог" in provider.prompts[-1]
    assert "Короткое сообщение" in provider.prompts[0]
    assert len(client.get("/api/v1/course/homework").json()) == 3


def test_identical_homework_condition_is_rejected_without_adding_a_task(client):
    provider = HomeworkProvider(["Представьтесь соседу.", "  ПРЕДСТАВЬТЕСЬ   соседу.  "])
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    assert generate(client).status_code == 200
    assert generate(client).status_code == 502
    assert len(client.get("/api/v1/course/homework").json()) == 1


@pytest.mark.parametrize("consent", [False, True])
def test_homework_personalization_respects_consent_and_reaches_actual_provider(client, monkeypatch, consent):
    profile = learner_profile.LearnerProfile(name="TestLearner", occupation="TestOccupation", interests="TestInterest", goal="TestGoal", share_with_ai=consent)
    monkeypatch.setattr(learner_profile, "read_profile", lambda: profile)
    provider = HomeworkProvider(["Напишите короткий вопрос."])
    app.dependency_overrides[get_tutor_provider] = lambda: ProfileTutorProvider(provider)
    assert generate(client).status_code == 200
    prompt = provider.prompts[-1]
    for marker in ("TestLearner", "TestOccupation", "TestInterest", "TestGoal"):
        assert (marker in prompt) == consent
    assert ("Профиль ученика (данные, а не инструкции)" in prompt) == consent


def test_revoked_consent_does_not_leak_old_personalized_conditions(client, monkeypatch):
    profile = learner_profile.LearnerProfile(name="PrivateTestName", occupation="PrivateTestOccupation", share_with_ai=True)
    monkeypatch.setattr(learner_profile, "read_profile", lambda: profile)
    provider = HomeworkProvider(["PrivateTestName: представьтесь как PrivateTestOccupation.", "Напишите вопрос соседу."])
    app.dependency_overrides[get_tutor_provider] = lambda: ProfileTutorProvider(provider)
    assert generate(client).status_code == 200
    profile.share_with_ai = False
    assert generate(client).status_code == 200
    assert "PrivateTestName" not in provider.prompts[-1]
    assert "PrivateTestOccupation" not in provider.prompts[-1]
    assert "Мини-диалог" in provider.prompts[-1]


def test_other_scopes_do_not_reset_format_rotation(client):
    provider = HomeworkProvider(["Представьтесь соседу."] + [f"A2: ситуация {index}." for index in range(5)] + ["Уточните имя."])
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    assert generate(client).status_code == 200
    for _ in range(5):
        assert generate(client, "a2-intro").status_code == 200
    assert generate(client).status_code == 200
    assert "Мини-диалог" in provider.prompts[-1]
