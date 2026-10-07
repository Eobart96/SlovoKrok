from types import SimpleNamespace

from app.routers import reports


def test_reports_persist_without_course_state(client, tmp_path, monkeypatch):
    monkeypatch.setattr(reports, "get_settings", lambda: SimpleNamespace(runtime_data_dir=tmp_path))
    assert client.get("/api/v1/reports").json() == []
    response = client.post("/api/v1/reports", json={"section": "reading", "description": "Не работает диктовка."})
    assert response.status_code == 201
    saved = response.json()
    assert set(saved) == {"id", "created_at", "section", "description", "location", "screenshots"}
    assert client.get("/api/v1/reports").json() == [saved]
    assert (tmp_path / "issue_reports.json").exists()


def test_corrupt_reports_are_not_overwritten(client, tmp_path, monkeypatch):
    monkeypatch.setattr(reports, "get_settings", lambda: SimpleNamespace(runtime_data_dir=tmp_path))
    path = tmp_path / "issue_reports.json"
    path.write_text("broken", encoding="utf-8")
    response = client.post("/api/v1/reports", json={"section": "reading", "description": "Описание проблемы."})
    assert response.status_code == 503
    assert path.read_text(encoding="utf-8") == "broken"


def test_reports_reject_extra_personal_fields(client):
    response = client.post("/api/v1/reports", json={"section": "reading", "description": "Описание проблемы.", "answers": ["Личный ответ"]})
    assert response.status_code == 422


def test_screenshots_export_and_confirmed_clear(client, tmp_path, monkeypatch):
    import base64
    import io
    import zipfile

    monkeypatch.setattr(reports, "get_settings", lambda: SimpleNamespace(runtime_data_dir=tmp_path))
    raw = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a0f8AAAAASUVORK5CYII=")
    screenshot = {"name": "../../shot.png", "mime": "image/png", "data": base64.b64encode(raw).decode()}
    payload = {"section": "reading", "description": "Ошибка чтения.", "screenshots": [screenshot]}
    saved = client.post("/api/v1/reports", json=payload)
    assert saved.status_code == 201
    assert client.get("/api/v1/reports").json()[0]["screenshots"] == [screenshot]
    exported = client.get("/api/v1/reports/export")
    assert exported.status_code == 200
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(exported.json()["data"]))) as archive:
        assert archive.read("screenshots/report_001_1.png") == raw
        assert "Ошибка чтения." in archive.read("SlovoKrok_обращения.txt").decode("utf-8-sig")
        assert not any(".." in name for name in archive.namelist())
    assert client.request("DELETE", "/api/v1/reports", json={}).status_code == 422
    assert len(client.get("/api/v1/reports").json()) == 1
    assert client.request("DELETE", "/api/v1/reports", json={"confirmation": "delete-all-reports"}).status_code == 200
    assert client.get("/api/v1/reports").json() == []


def test_invalid_screenshots_rejected(client):
    import base64
    payload = {"section": "reading", "description": "Ошибка чтения.", "screenshots": [{"name": "shot.png", "mime": "image/png", "data": base64.b64encode(b"not an image").decode()}]}
    assert client.post("/api/v1/reports", json=payload).status_code == 422
    payload["screenshots"][0]["data"] = "%%%"
    assert client.post("/api/v1/reports", json=payload).status_code == 422
    payload["screenshots"] *= 4
    assert client.post("/api/v1/reports", json=payload).status_code == 422


def test_reports_save_location_and_reject_answers_in_context(client, tmp_path, monkeypatch):
    monkeypatch.setattr(reports, "get_settings", lambda: SimpleNamespace(runtime_data_dir=tmp_path))
    location = {"view": "reading", "task_type": "reading", "task_id": "12", "task_title": "Знакомство", "scope": "Модуль 1"}
    response = client.post("/api/v1/reports", json={"section": "reading", "description": "Ошибка в тексте.", "location": location})
    assert response.status_code == 201
    assert client.get("/api/v1/reports").json()[0]["location"]["task_id"] == "12"
    response = client.post("/api/v1/reports", json={"section": "reading", "description": "Ошибка в тексте.", "location": {"answer": "Личный ответ"}})
    assert response.status_code == 422
