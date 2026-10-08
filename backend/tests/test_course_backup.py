from copy import deepcopy
import re

import pytest

from app.database import get_db
from app.dependencies import get_tutor_provider
from app.main import app
from app.models import CourseExercise
from tests.test_interactive_api import InteractiveTutorProvider, _state_headers, _state_payload


def current_state_headers(client) -> dict[str, str]:
    return _state_headers(client.get("/api/v1/course/state").json()["revision"])


def seed(client):
    app.dependency_overrides[get_tutor_provider] = lambda: InteractiveTutorProvider()
    client.put("/api/v1/course/state", json=_state_payload(), headers=_state_headers(None)).raise_for_status()
    payload = {"lesson_slug": "greetings", "lesson_title": "Приветствия", "theory": "Dobrý deň"}
    exercise = client.post("/api/v1/course/exercises", json=payload).json()
    client.post(f"/api/v1/course/exercises/{exercise['id']}/answer", json={"answer": "Dobrý deň"}).raise_for_status()
    reading = client.post("/api/v1/course/readings", json={**payload, "completed_theory": ""}).json()
    client.post(f"/api/v1/course/readings/{reading['id']}/check", json={"retelling": "Анна представилась"}).raise_for_status()
    homework = client.post("/api/v1/course/homework", json={**payload, "known_mistakes": []}).json()
    client.post(f"/api/v1/course/homework/{homework['id']}/submit", json={"answer": "Dobrý deň"}).raise_for_status()
    client.put("/api/v1/course/vocabulary/sync", json={"items": [{"lesson_slug": "greetings", "lesson_title": "Приветствия", "word": "Dobrý deň", "translation": "Здравствуйте", "example": None}]}).raise_for_status()
    translated = client.post("/api/v1/tutor/translate", json={"direction": "ru-sk", "text": "Спасибо."}).json()
    client.post("/api/v1/tutor/translate-question", json={
        "history_id": translated["history_id"], "source_text": "Спасибо.", "translation": "Ďakujem.",
        "direction": "ru-sk", "question": "Почему эта форма?",
    }).raise_for_status()


def test_backup_roundtrip_preserves_relationships_and_existing_data(client):
    seed(client)
    state = _state_payload()
    state.update({
        "activeLevel": "A2",
        "activeModule": 2,
        "selectedSlug": "a2-nominative-plural-things",
        "levelPositions": {"A1": {"activeModule": 1, "selectedSlug": "greetings"}, "A2": {"activeModule": 2, "selectedSlug": "a2-nominative-plural-things"}},
        "finalCompletedModules": {"a1:1": True, "a2:2": False},
    })
    state["personalCheatSheets"] = [{
        "id": "note-1", "title": "Моё правило", "content": "После do — Genitív.",
        "createdAt": "2026-09-13T12:00:00Z", "updatedAt": "2026-09-13T12:00:00Z",
    }]
    state["mistakes"] = {
        "m1": {
            "id": "m1", "lessonSlug": "greetings", "prompt": "Pozdravte.",
            "answer": "Dobrý deň.", "attempts": 1, "mastered": False,
        }
    }
    client.put("/api/v1/course/state", json=state, headers=current_state_headers(client)).raise_for_status()
    backup = client.get("/api/v1/course/backup").json()
    assert set(backup) == {"format", "version", "exported_at", "state", "tables"}
    assert backup["version"] == 2
    assert all(len(rows) == 1 for rows in backup["tables"].values())
    before = client.get("/api/v1/course/state").json()
    preview = client.post("/api/v1/course/backup/validate", json=backup)
    assert preview.status_code == 200
    assert client.get("/api/v1/course/state").json() == before  # read-only preview
    # Remove test materials through ordinary endpoints, then create colliding IDs.
    for name in ("exercises", "readings", "homework"):
        client.delete(f"/api/v1/course/{name}/1").raise_for_status()
    client.delete("/api/v1/tutor/translation-history/1").raise_for_status()
    payload = {"lesson_slug": "greetings", "lesson_title": "Other", "theory": "Other"}
    client.post("/api/v1/course/exercises", json=payload).raise_for_status()
    client.post("/api/v1/course/vocabulary/1/review").raise_for_status()
    changed = _state_payload(); changed["fontSize"] = "normal"
    client.put("/api/v1/course/state", json=changed, headers=current_state_headers(client)).raise_for_status()
    for _ in range(2):
        restored = client.post("/api/v1/course/backup/restore", json=backup, headers=current_state_headers(client))
        assert restored.status_code == 200
        assert restored.json()["state"]["fontSize"] == "large"
        assert restored.json()["state"]["levelPositions"] == state["levelPositions"]
    after = client.get("/api/v1/course/backup").json()
    assert len(after["tables"]["exercises"]) == 2
    assert len(after["tables"]["exercise_attempts"]) == 1
    attempt = after["tables"]["exercise_attempts"][0]
    parent = next(row for row in after["tables"]["exercises"] if row["id"] == attempt["exercise_id"])
    assert parent["lesson_title"] == "Приветствия"
    assert after["tables"]["vocabulary"][0]["review_count"] == 1
    assert len(after["tables"]["homework_attempts"]) == 1
    assert len(after["tables"]["reading_attempts"]) == 1
    assert len(after["tables"]["translation_history"]) == 1
    assert len(after["tables"]["translation_questions"]) == 1
    assert after["state"]["personalCheatSheets"][0]["title"] == "Моё правило"
    assert after["state"]["mistakes"]["m1"]["answer"] == "Dobrý deň."
    assert after["state"]["activeLevel"] == "A2"
    assert after["state"]["finalCompletedModules"] == {"a1:1": True, "a2:2": False}


def test_backup_roundtrip_preserves_reading_tasks_and_attempts(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    assert len(backup["tables"]["readings"]) == 1
    assert len(backup["tables"]["reading_attempts"]) == 1

    reading_id = backup["tables"]["readings"][0]["id"]
    client.delete(f"/api/v1/course/readings/{reading_id}").raise_for_status()
    assert client.get("/api/v1/course/readings").json() == []

    restored = client.post(
        "/api/v1/course/backup/restore",
        json=backup,
        headers=current_state_headers(client),
    )
    assert restored.status_code == 200
    readings = client.get("/api/v1/course/readings").json()
    assert len(readings) == 1
    assert readings[0]["title"] == "Приветствие"
    assert readings[0]["latest_attempt"]["retelling"] == "Анна представилась"
    assert readings[0]["offline_ready"] is True


def task_mistake(identifier):
    return {
        "id": identifier, "lessonSlug": "greetings", "prompt": "Pozdravte.",
        "answer": "Dobrý deň.", "attempts": 3, "mastered": False,
        "reviewStage": 1, "dueAt": "2026-10-10T12:00:00Z",
        "reviewTask": {
            "prompt": "Pozdravte.", "learnerAnswer": "Dobry den.",
            "explanation": "Doplňte dĺžne.", "kind": "exact",
        },
    }


def test_restore_remaps_task_mistake_keys_and_ids_without_changing_other_state(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    # ID 1 belongs to a different local task than the archive task in each table.
    for table in ("exercises", "homework"):
        backup["tables"][table][0]["lesson_title"] = f"Archived {table}"
    backup["state"]["mistakes"] = {
        identifier: task_mistake(identifier)
        for identifier in ("exercise:1", "homework:1", "greetings-check-1")
    }
    backup["state"]["mistakes"]["homework:1"]["reviewTask"]["kind"] = "open"
    original = deepcopy(backup)
    previous_mistakes = None
    for _ in range(2):
        response = client.post(
            "/api/v1/course/backup/restore", json=backup,
            headers=current_state_headers(client),
        )
        response.raise_for_status()
        restored = client.get("/api/v1/course/backup").json()
        expected = deepcopy(backup["state"])
        for kind, table in (("exercise", "exercises"), ("homework", "homework")):
            rows = restored["tables"][table]
            assert len(rows) == 2
            assert next(row for row in rows if row["id"] == 1)["lesson_title"] == "Приветствия"
            task = next(row for row in rows if row["lesson_title"] == f"Archived {table}")
            assert task["id"] != 1
            identifier = f"{kind}:{task['id']}"
            mistake = expected["mistakes"].pop(f"{kind}:1")
            mistake["id"] = identifier
            expected["mistakes"][identifier] = mistake
        assert restored["state"] == expected
        if previous_mistakes is not None:
            assert restored["state"]["mistakes"] == previous_mistakes
        previous_mistakes = restored["state"]["mistakes"]
    assert backup == original  # Restoring must not mutate the supplied archive.


def test_restore_retains_deleted_task_reviews_without_linking_local_tasks(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    for table in ("exercises", "exercise_attempts", "homework", "homework_attempts"):
        backup["tables"][table] = []
    backup["state"]["mistakes"] = {
        identifier: task_mistake(identifier)
        for identifier in ("exercise:1", "homework:1", "greetings-check-1")
    }
    previous_mistakes = None
    for archive in (backup, backup):
        client.post(
            "/api/v1/course/backup/restore", json=archive,
            headers=current_state_headers(client),
        ).raise_for_status()
        restored = client.get("/api/v1/course/backup").json()
        mistakes = restored["state"]["mistakes"]
        assert len(mistakes) == 3
        assert mistakes["greetings-check-1"] == backup["state"]["mistakes"]["greetings-check-1"]
        for kind, table in (("exercise", "exercises"), ("homework", "homework")):
            assert len(restored["tables"][table]) == 1
            identifier = next(key for key in mistakes if key.startswith(f"detached:{kind}:"))
            assert re.fullmatch(r"(exercise|homework):[0-9]+", identifier) is None
            expected = deepcopy(backup["state"]["mistakes"][f"{kind}:1"])
            expected["id"] = identifier
            assert mistakes[identifier] == expected
        if previous_mistakes is not None:
            assert mistakes == previous_mistakes
        previous_mistakes = mistakes
    # Detached reviews remain detached when a restored course is exported again.
    client.post(
        "/api/v1/course/backup/restore", json=restored,
        headers=current_state_headers(client),
    ).raise_for_status()
    assert client.get("/api/v1/course/backup").json()["state"]["mistakes"] == previous_mistakes


def test_restore_keeps_both_reviews_when_identical_archive_tasks_share_one_target(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    duplicate = deepcopy(backup["tables"]["exercises"][0])
    duplicate["id"] = 2
    backup["tables"]["exercises"].append(duplicate)
    backup["state"]["mistakes"] = {
        identifier: task_mistake(identifier) for identifier in ("exercise:1", "exercise:2")
    }
    backup["state"]["mistakes"]["exercise:2"]["prompt"] = "Second saved review"
    previous = None
    for _ in range(2):
        client.post(
            "/api/v1/course/backup/restore", json=backup,
            headers=current_state_headers(client),
        ).raise_for_status()
        restored = client.get("/api/v1/course/backup").json()
        assert len(restored["tables"]["exercises"]) == 1
        mistakes = restored["state"]["mistakes"]
        assert len(mistakes) == 2
        assert mistakes["exercise:1"] == backup["state"]["mistakes"]["exercise:1"]
        detached = next(value for key, value in mistakes.items() if key.startswith("detached:exercise:"))
        expected = deepcopy(backup["state"]["mistakes"]["exercise:2"])
        expected["id"] = detached["id"]
        assert detached == expected
        if previous is not None:
            assert mistakes == previous
        previous = mistakes


def test_backup_preserves_homework_and_exercise_offline_references(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    assert backup["tables"]["exercises"][0]["theory_snapshot"]
    assert backup["tables"]["homework"][0]["reference_answer"] == "Dobrý deň. Volám sa Anna."

    client.delete("/api/v1/course/exercises/1").raise_for_status()
    client.delete("/api/v1/course/homework/1").raise_for_status()
    client.post(
        "/api/v1/course/backup/restore",
        json=backup,
        headers=current_state_headers(client),
    ).raise_for_status()

    exercises = client.get("/api/v1/course/exercises").json()
    homework = client.get("/api/v1/course/homework").json()
    assert len(exercises) == 1
    assert len(homework) == 1
    assert homework[0]["offline_ready"] is True


def test_backup_version_1_remains_compatible_without_translation_history(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    backup["version"] = 1
    backup["tables"].pop("translation_history")
    backup["tables"].pop("translation_questions")

    assert client.post("/api/v1/course/backup/validate", json=backup).status_code == 200
    restored = client.post("/api/v1/course/backup/restore", json=backup, headers=current_state_headers(client))
    assert restored.status_code == 200


def test_large_restore_does_not_query_once_per_record(client, monkeypatch):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    source = backup["tables"]["vocabulary"][0]
    for item_id in range(2, 2_002):
        item = deepcopy(source)
        item.update({"id": item_id, "word": f"word-{item_id}", "translation": f"translation-{item_id}"})
        backup["tables"]["vocabulary"].append(item)

    from sqlalchemy.orm import Session
    original_scalar = Session.scalar
    scalar_calls = 0

    def count_scalar(self, *args, **kwargs):
        nonlocal scalar_calls
        scalar_calls += 1
        return original_scalar(self, *args, **kwargs)

    monkeypatch.setattr(Session, "scalar", count_scalar)
    restored = client.post(
        "/api/v1/course/backup/restore",
        json=backup,
        headers=current_state_headers(client),
    )

    assert restored.status_code == 200
    assert scalar_calls < 10
    assert len(client.get("/api/v1/course/backup").json()["tables"]["vocabulary"]) == 2_001


def test_invalid_backups_never_modify_state(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    before = client.get("/api/v1/course/state").json()
    before_history = client.get("/api/v1/tutor/translation-history").json()
    invalid = []
    b = deepcopy(backup); b["version"] = 999; invalid.append(b)
    b = deepcopy(backup); b["tables"]["settings"] = []; invalid.append(b)
    b = deepcopy(backup); b["tables"]["exercise_attempts"][0]["exercise_id"] = 900; invalid.append(b)
    b = deepcopy(backup); b["tables"]["vocabulary"].append(b["tables"]["vocabulary"][0]); invalid.append(b)
    b = deepcopy(backup); b["tables"]["exercises"][0]["surprise"] = "unexpected"; invalid.append(b)
    b = deepcopy(backup); b["state"]["progress"] = {"greetings": "invalid"}; invalid.append(b)
    b = deepcopy(backup); b["tables"]["translation_history"][0]["direction"] = "xxxxx"; invalid.append(b)
    b = deepcopy(backup); b["tables"]["translation_history"][0]["alternatives_json"] = '{"not":"a list"}'; invalid.append(b)
    b = deepcopy(backup); b["tables"]["translation_questions"][0]["question"] = "x" * 1_001; invalid.append(b)
    for malformed in invalid:
        assert client.post("/api/v1/course/backup/restore", json=malformed).status_code == 422
        assert client.get("/api/v1/course/state").json() == before
        assert client.get("/api/v1/tutor/translation-history").json() == before_history
    assert client.post("/api/v1/course/backup/validate", content=b"x" * (10 * 1024 * 1024 + 1)).status_code == 413


@pytest.mark.parametrize("snapshot", [
    "slovokrok-exercise:v1:[]",
    "slovokrok-exercise:v1:{\"interaction_type\":\"text\"}",
    "slovokrok-exercise:v1:{\"theory\":\"Pozdravte.\",\"interaction_type\":\"choice\",\"options\":[\"one\"]}",
])
def test_invalid_exercise_snapshot_backup_is_exportable_but_rejected_on_import(client, snapshot):
    seed(client)
    # Simulate a record imported by an older version, only in the synthetic DB.
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        db.get(CourseExercise, 1).theory_snapshot = snapshot
        db.commit()
    finally:
        database_provider.close()
    response = client.get("/api/v1/course/backup")
    response.raise_for_status()
    backup = response.json()
    assert backup["tables"]["exercises"][0]["theory_snapshot"] == snapshot
    before = client.get("/api/v1/course/state").json()
    for operation in ("validate", "restore"):
        response = client.post(
            f"/api/v1/course/backup/{operation}", json=backup,
            headers=current_state_headers(client),
        )
        assert response.status_code == 422
        assert client.get("/api/v1/course/state").json() == before
        after = client.get("/api/v1/course/backup").json()
        assert after["state"] == backup["state"]
        assert after["tables"] == backup["tables"]


def test_backup_import_still_accepts_legacy_plain_exercise_theory(client):
    seed(client)
    backup = client.get("/api/v1/course/backup").json()
    backup["tables"]["exercises"][0]["theory_snapshot"] = "Dobrý deň. Legacy plain theory."
    assert client.post("/api/v1/course/backup/validate", json=backup).status_code == 200
    client.post(
        "/api/v1/course/backup/restore", json=backup,
        headers=current_state_headers(client),
    ).raise_for_status()
    restored = client.get("/api/v1/course/backup").json()
    assert any(
        row["theory_snapshot"] == "Dobrý deň. Legacy plain theory."
        for row in restored["tables"]["exercises"]
    )


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
        client.post("/api/v1/course/backup/restore", json=backup, headers=current_state_headers(client))
    assert client.get("/api/v1/course/exercises").json() == []
