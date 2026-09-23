import json

import pytest
from sqlalchemy.orm import Session

from app.models import CourseState, utc_now
import app.services.startup as startup_module
from tests.test_interactive_api import _state_headers, _state_payload


def test_state_write_requires_a_well_formed_revision(client):
    missing = client.put("/api/v1/course/state", json=_state_payload())
    assert missing.status_code == 428

    malformed = client.put(
        "/api/v1/course/state",
        json=_state_payload(),
        headers={"X-Course-State-Revision": "not-a-revision"},
    )
    assert malformed.status_code == 400


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.update({"surprise": True}),
        lambda value: value["progress"].update({"greetings": "unknown"}),
        lambda value: value["lessonSteps"].update({"greetings": -1}),
        lambda value: value["practiceResults"].update({"practice-1": 1}),
        lambda value: value["mistakes"].update({
            "m1": {
                "id": "m1", "lessonSlug": "greetings", "prompt": "P", "answer": "A",
                "attempts": 1, "mastered": False, "surprise": "no",
            }
        }),
    ],
)
def test_state_rejects_unknown_fields_and_invalid_nested_values(client, mutate):
    payload = _state_payload()
    mutate(payload)
    response = client.put("/api/v1/course/state", json=payload, headers=_state_headers(None))
    assert response.status_code == 422
    assert client.get("/api/v1/course/state").json()["exists"] is False


def test_legacy_schema_is_read_with_defaults_and_upgraded_on_save(client):
    with Session(startup_module.engine) as db:
        db.add(CourseState(
            id=1,
            schema_version=1,
            state_json=json.dumps({"progress": {"greetings": "completed"}}),
            updated_at=utc_now(),
        ))
        db.commit()

    legacy = client.get("/api/v1/course/state")
    assert legacy.status_code == 200
    assert legacy.json()["schema_version"] == 1
    assert legacy.json()["state"]["activeModule"] == 1
    assert legacy.json()["state"]["personalCheatSheets"] == []

    upgraded = client.put(
        "/api/v1/course/state",
        json=legacy.json()["state"],
        headers=_state_headers(legacy.json()["revision"]),
    )
    assert upgraded.status_code == 200
    assert upgraded.json()["schema_version"] == 2
    assert upgraded.json()["revision"] != legacy.json()["revision"]


def test_strict_nested_state_round_trip_preserves_supported_fields(client):
    payload = _state_payload()
    payload["lessonSteps"] = {"greetings": 2}
    payload["practiceResults"] = {"greeting-practice": True}
    payload["mistakes"] = {
        "m1": {
            "id": "m1", "lessonSlug": "greetings", "prompt": "Pozdravte.",
            "answer": "Dobrý deň.", "attempts": 2, "mastered": False,
            "reviewStage": 1, "dueAt": "2026-09-20T12:00:00Z",
        }
    }
    payload["chatHistories"] = {
        "greetings": [{
            "id": 1, "role": "assistant", "text": "Ako sa voláte?",
            "suggestions": ["Volám sa Anna."], "interactionKind": "answer",
        }]
    }
    payload["lessonSummaries"] = {
        "greetings": {
            "understanding": 80, "level": "Хорошая основа", "strengths": ["Приветствие"],
            "mistakes": ["Порядок слов"], "review": ["Повторить завтра"], "userTurns": 3,
            "evidence": {"coreCorrect": 4, "coreTotal": 5},
        }
    }

    saved = client.put("/api/v1/course/state", json=payload, headers=_state_headers(None))
    assert saved.status_code == 200
    restored = client.get("/api/v1/course/state").json()
    assert restored["revision"] == saved.json()["revision"]
    assert restored["state"]["mistakes"]["m1"]["attempts"] == 2
    assert restored["state"]["chatHistories"]["greetings"][0]["suggestions"] == ["Volám sa Anna."]
    assert restored["state"]["lessonSummaries"]["greetings"]["evidence"]["coreTotal"] == 5


def test_stale_state_write_returns_conflict_without_overwriting_newer_progress(client):
    created = client.put("/api/v1/course/state", json=_state_payload(), headers=_state_headers(None))
    assert created.status_code == 200
    stale_revision = created.json()["revision"]

    newer = _state_payload()
    newer["fontSize"] = "normal"
    saved = client.put("/api/v1/course/state", json=newer, headers=_state_headers(stale_revision))
    assert saved.status_code == 200
    assert saved.json()["revision"] != stale_revision

    stale = _state_payload()
    stale["fontSize"] = "extra-large"
    conflict = client.put("/api/v1/course/state", json=stale, headers=_state_headers(stale_revision))
    assert conflict.status_code == 409

    current = client.get("/api/v1/course/state").json()
    assert current["revision"] == saved.json()["revision"]
    assert current["state"]["fontSize"] == "normal"


def test_stale_backup_restore_cannot_replace_newer_progress(client):
    created = client.put("/api/v1/course/state", json=_state_payload(), headers=_state_headers(None))
    stale_revision = created.json()["revision"]
    backup = client.get("/api/v1/course/backup").json()

    newer = _state_payload()
    newer["fontSize"] = "normal"
    saved = client.put("/api/v1/course/state", json=newer, headers=_state_headers(stale_revision))
    assert saved.status_code == 200

    conflict = client.post(
        "/api/v1/course/backup/restore",
        json=backup,
        headers=_state_headers(stale_revision),
    )
    assert conflict.status_code == 409
    current = client.get("/api/v1/course/state").json()
    assert current["revision"] == saved.json()["revision"]
    assert current["state"]["fontSize"] == "normal"
