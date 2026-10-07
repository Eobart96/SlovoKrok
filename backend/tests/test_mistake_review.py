import json

from app.dependencies import get_tutor_provider
from app.main import app
from app.database import get_db
from app.models import CourseExercise
from app.tutor import parse_generated_exercise, encode_exercise_snapshot
from app.schemas.course import CourseMistakePayload


def payload(**changes):
    return {"prompt": "Поздоровайтесь.", "expected_answer": "Dobrý deň.", "answer": "dobrý   deň!", "kind": "exact", **changes}


def test_reference_review_does_not_call_provider_and_survives_deleted_source(client):
    class MustNotRun:
        def respond(self, context):
            raise AssertionError("Reference review called AI")
    app.dependency_overrides[get_tutor_provider] = MustNotRun
    response = client.post("/api/v1/course/mistakes/check", json=payload(source_exercise_id=999999))
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["score"] == 100
    response = client.post("/api/v1/course/mistakes/check", json=payload(answer="Dobry den"))
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_pair_review_accepts_different_pair_order(client):
    response = client.post("/api/v1/course/mistakes/check", json=payload(expected_answer="Ahoj → Привет; Dovidenia → До свидания", answer="Dovidenia→До свидания; Ahoj→Привет"))
    assert response.status_code == 200
    assert response.json()["is_correct"] is True


def test_reference_review_accepts_known_alternative(client):
    response = client.post("/api/v1/course/mistakes/check", json=payload(answer="Do videnia", expected_answer="Dovidenia", accepted_answers=["Do videnia"]))
    assert response.status_code == 200
    assert response.json()["is_correct"] is True


def test_restored_mistake_does_not_use_different_source_with_same_id(client):
    database_provider = app.dependency_overrides[get_db]()
    db = next(database_provider)
    try:
        generated = parse_generated_exercise('{"question":"Скажи привет.","instruction":"Введите ответ.","interaction_type":"text","accepted_answers":["Ahoj"]}')
        exercise = CourseExercise(lesson_slug="greetings", lesson_title="Приветствия", question=generated.question, instruction=generated.instruction, theory_snapshot=encode_exercise_snapshot("Ahoj", generated))
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        source_id = exercise.id
    finally:
        database_provider.close()
    response = client.post("/api/v1/course/mistakes/check", json=payload(source_exercise_id=source_id))
    assert response.status_code == 200
    assert response.json()["is_correct"] is True


def test_open_review_accepts_provider_assessment_with_schema(client):
    class Provider:
        def respond(self, context):
            assert context.response_schema is not None
            return json.dumps({"is_correct": True, "score": 100, "corrected_answer": "Dobrý deň.", "explanation": "Верно.", "next_exercise": "Повторите позже."})
    app.dependency_overrides[get_tutor_provider] = Provider
    response = client.post("/api/v1/course/mistakes/check", json=payload(kind="open"))
    assert response.status_code == 200
    assert response.json()["is_correct"] is True


def test_mistake_snapshot_is_optional_and_roundtrips():
    old = {"id": "homework:1", "lessonSlug": "greetings", "prompt": "Задание", "answer": "Dobrý deň.", "attempts": 1, "mastered": False}
    assert CourseMistakePayload.model_validate(old).reviewTask is None
    snapshot = {"prompt": "Поздоровайтесь.", "learnerAnswer": "Dobry den", "explanation": "Нужны знаки.", "kind": "open"}
    new = CourseMistakePayload.model_validate({**old, "reviewTask": snapshot})
    assert CourseMistakePayload.model_validate_json(new.model_dump_json()).reviewTask.model_dump() == snapshot
