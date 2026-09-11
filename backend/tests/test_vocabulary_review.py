from datetime import datetime, timedelta, timezone


def test_ratings_change_schedule_without_losing_review_history(client):
    vocabulary = client.put("/api/v1/course/vocabulary/sync", json={"items": [{"lesson_slug": "greetings", "lesson_title": "Приветствия", "word": "Dobrý deň", "translation": "Здравствуйте", "example": None}]}).json()
    url = f"/api/v1/course/vocabulary/{vocabulary[0]['id']}/review"
    legacy = client.post(url).json()
    assert legacy["interval_days"] == 1
    easy = client.post(url, json={"rating": "easy"}).json()
    assert easy["interval_days"] == 3
    assert client.post(url, json={"rating": "easy"}).json()["interval_days"] == 6
    assert client.post(url, json={"rating": "hard"}).json()["interval_days"] == 3
    before = datetime.now(timezone.utc)
    forgotten = client.post(url, json={"rating": "again"}).json()
    assert forgotten["review_count"] == 5
    assert forgotten["interval_days"] == 0
    assert not forgotten["is_due"]
    due = datetime.fromisoformat(forgotten["next_review_at"]).replace(tzinfo=timezone.utc)
    assert before + timedelta(minutes=9) < due < before + timedelta(minutes=11)
    assert client.post(url, json={"rating": "invalid"}).status_code == 422
    assert client.get("/api/v1/course/vocabulary").json()[0]["review_count"] == 5
    for _ in range(8):
        latest = client.post(url, json={"rating": "easy"}).json()
    assert latest["interval_days"] == 30
