from copy import deepcopy

from app.dependencies import get_tutor_provider
from app.main import app
from tests.test_interactive_api import InteractiveTutorProvider, _state_payload


def seed(client):
    app.dependency_overrides[get_tutor_provider] = lambda: InteractiveTutorProvider()
    client.put("/api/v1/course/state", json=_state_payload()).raise_for_status()
    payload = {"lesson_slug": "greetings", "lesson_title": "Приветствия", "theory": "Dobrý deň"}
    exercise = client.post("/api/v1/course/exercises", json=payload).json()
    client.post(f"/api/v1/course/exercises/{exercise['id']}/answer", json={"answer": "Dobrý deň"}).raise_for_status()
    reading = client.post("/api/v1/course/readings", json={**payload, "completed_theory": ""}).json()
    client.post(f"/api/v1/course/readings/{reading['id']}/check", json={"retelling": "Анна представилась"}).raise_for_status()
    homework = client.post("/api/v1/course/homework", json={**payload, "known_mistakes": []}).json()
    client.post(f"/api/v1/course/homework/{homework['id']}/submit", json={"answer": "Dobrý deň"}).raise_for_status()
    client.put("/api/v1/course/vocabulary/sync", json={"items": [{"lesson_slug": "greetings", "lesson_title": "Приветствия", "word": "Dobrý deň", "translation": "Здравствуйте", "example": None}]}).raise_for_status()


def test_backup_roundtrip_preserves_relationships_and_existing_data(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    assert set(backup) == {"format", "version", "exported_at", "state", "tables"}
    assert all(len(rows) == 1 for rows in backup["tables"].values())
    before = client.get("/api/v1/course/state").json()
    preview = client.post("/api/v1/course/backup/validate", json=backup)
    assert preview.status_code == 200
    assert client.get("/api/v1/course/state").json() == before  # read-only preview
    # Remove test materials through ordinary endpoints, then create colliding IDs.
    for name in ("exercises", "readings", "homework"):
        client.delete(f"/api/v1/course/{name}/1").raise_for_status()
    payload = {"lesson_slug": "greetings", "lesson_title": "Other", "theory": "Other"}
    client.post("/api/v1/course/exercises", json=payload).raise_for_status()
    client.post("/api/v1/course/vocabulary/1/review").raise_for_status()
    changed = _state_payload(); changed["fontSize"] = "normal"
    client.put("/api/v1/course/state", json=changed).raise_for_status()
    for _ in range(2):
        restored = client.post("/api/v1/course/backup/restore", json=backup)
        assert restored.status_code == 200
        assert restored.json()["state"]["fontSize"] == "large"
    after = client.get("/api/v1/course/backup").json()
    assert len(after["tables"]["exercises"]) == 2
    assert len(after["tables"]["exercise_attempts"]) == 1
    attempt = after["tables"]["exercise_attempts"][0]
    parent = next(row for row in after["tables"]["exercises"] if row["id"] == attempt["exercise_id"])
    assert parent["lesson_title"] == "Приветствия"
    assert after["tables"]["vocabulary"][0]["review_count"] == 1
    assert len(after["tables"]["homework_attempts"]) == 1
    assert len(after["tables"]["reading_attempts"]) == 1


def test_invalid_backups_never_modify_state(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    before = client.get("/api/v1/course/state").json()
    invalid = []
    b = deepcopy(backup); b["version"] = 999; invalid.append(b)
    b = deepcopy(backup); b["tables"]["settings"] = []; invalid.append(b)
    b = deepcopy(backup); b["tables"]["exercise_attempts"][0]["exercise_id"] = 900; invalid.append(b)
    b = deepcopy(backup); b["tables"]["vocabulary"].append(b["tables"]["vocabulary"][0]); invalid.append(b)
    b = deepcopy(backup); b["tables"]["exercises"][0]["surprise"] = "unexpected"; invalid.append(b)
    b = deepcopy(backup); b["state"]["progress"] = {"greetings": "invalid"}; invalid.append(b)
    for malformed in invalid:
        assert client.post("/api/v1/course/backup/restore", json=malformed).status_code == 422
        assert client.get("/api/v1/course/state").json() == before
    assert client.post("/api/v1/course/backup/validate", content=b"x" * (10 * 1024 * 1024 + 1)).status_code == 413


def test_restore_rolls_back_all_insertions_on_failure(client, monkeypatch):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    client.delete("/api/v1/course/exercises/1").raise_for_status()
    from sqlalchemy.orm import Session
    original = Session.flush
    def fail_on_attempt(self, *args, **kwargs):
        from app.models import CourseExerciseAttempt
        if any(isinstance(row, CourseExerciseAttempt) for row in self.new):
            raise RuntimeError("test transaction failure")
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Session, "flush", fail_on_attempt)
    import pytest
    with pytest.raises(RuntimeError, match="test transaction failure"):
        client.post("/api/v1/course/backup/restore", json=backup)
    assert client.get("/api/v1/course/exercises").json() == []
