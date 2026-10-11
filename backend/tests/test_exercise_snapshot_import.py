import pytest
import json

from app.database import get_db
from app.main import app
from app.models import CourseExercise
from app.tutor_core.exercise import decode_exercise_snapshot


def test_legacy_order_is_repaired_on_listing_without_rewriting_saved_snapshot(client):
    snapshot = "slovokrok-exercise:v1:" + json.dumps({"theory": "Old theory", "interaction_type": "order", "tokens": ["Kuriér", "Sergej", "je."], "accepted_answers": ["Sergej je kuriér."]})
    assert client.post("/api/v1/course/materials/import", json=collection(snapshot)).status_code == 200
    exercise = client.get("/api/v1/course/exercises").json()[0]
    assert exercise["tokens"] == ["kuriér.", "Sergej", "je"]
    attempt = client.post(f"/api/v1/course/exercises/{exercise['id']}/answer", json={"answer": "Sergej je kuriér.", "assessment_mode": "offline"})
    assert attempt.status_code == 200
    assert attempt.json()["is_correct"] is True
    exported = client.get("/api/v1/course/materials/export").json()
    assert exported["exercises"][0]["theory_snapshot"] == snapshot


def collection(snapshot):
    return {
        "format": "slovokrok-course-materials", "version": 1,
        "exported_at": "2026-10-08T00:00:00Z",
        "exercises": [{
            "lesson_slug": "greetings", "lesson_title": "Приветствия",
            "question": "Поздоровайтесь", "instruction": "Введите ответ",
            "theory_snapshot": snapshot, "created_at": "2026-10-08T00:00:00Z",
        }], "readings": [], "homework": [],
    }


@pytest.mark.parametrize("payload", ["{}", "[]", "null", "1", '{"theory":null}', '{"theory":"x","interaction_type":"choice"}', "{broken", "[" * 1500 + "]" * 1500])
def test_bad_versioned_import_rejected_without_partial_writes(client, payload):
    data = collection("slovokrok-exercise:v1:" + payload)
    good = collection("Dobrý deň.")["exercises"][0]
    data["exercises"].insert(0, good)
    assert client.post("/api/v1/course/materials/import", json=data).status_code == 422
    assert client.get("/api/v1/course/exercises").json() == []


@pytest.mark.parametrize("snapshot", ["Dobrý deň.", 'slovokrok-exercise:v1:{"theory":"Dobrý deň.","interaction_type":"choice","options":["Dobrý deň.","Ahoj."],"accepted_answers":["Dobrý deň."]}'])
def test_valid_and_legacy_snapshots_still_import_and_reimport(client, snapshot):
    data = collection(snapshot)
    assert client.post("/api/v1/course/materials/import", json=data).json()["exercises"]["imported"] == 1
    assert client.post("/api/v1/course/materials/import", json=data).json()["exercises"]["skipped"] == 1
    listed = client.get("/api/v1/course/exercises")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


@pytest.mark.parametrize("payload", ["{}", "[]", "null", '{"theory":false}', "{broken", "[" * 1500 + "]" * 1500])
def test_preexisting_broken_snapshots_do_not_break_readonly_listing(client, payload):
    provider = app.dependency_overrides[get_db]()
    db = next(provider)
    try:
        db.add(CourseExercise(lesson_slug="greetings", lesson_title="Old import", question="Поздоровайтесь", instruction="Ответьте", theory_snapshot="slovokrok-exercise:v1:" + payload))
        db.commit()
    finally:
        provider.close()
    listed = client.get("/api/v1/course/exercises")
    assert listed.status_code == 200
    assert listed.json()[0]["interaction_type"] == "text"
    # Safety exports must not become unavailable because of old bad data.
    exported = client.get("/api/v1/course/materials/export")
    assert exported.status_code == 200
    assert exported.json()["exercises"][0]["theory_snapshot"] == "slovokrok-exercise:v1:" + payload
    theory, interaction = decode_exercise_snapshot("slovokrok-exercise:v1:" + payload)
    assert theory == ""
    assert interaction.accepted_answers == []
