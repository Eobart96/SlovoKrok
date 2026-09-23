from app.main import app


EXPECTED_COURSE_AND_TUTOR_ROUTES = {
    ("GET", "/api/v1/course/state"),
    ("PUT", "/api/v1/course/state"),
    ("GET", "/api/v1/course/exercises"),
    ("POST", "/api/v1/course/exercises"),
    ("DELETE", "/api/v1/course/exercises"),
    ("POST", "/api/v1/course/exercises/{exercise_id}/answer"),
    ("DELETE", "/api/v1/course/exercises/{exercise_id}"),
    ("GET", "/api/v1/course/readings"),
    ("POST", "/api/v1/course/readings"),
    ("POST", "/api/v1/course/readings/{reading_id}/check"),
    ("DELETE", "/api/v1/course/readings/{reading_id}"),
    ("PUT", "/api/v1/course/vocabulary/sync"),
    ("GET", "/api/v1/course/vocabulary"),
    ("POST", "/api/v1/course/vocabulary/{item_id}/review"),
    ("GET", "/api/v1/course/homework"),
    ("POST", "/api/v1/course/homework"),
    ("POST", "/api/v1/course/homework/{homework_id}/submit"),
    ("DELETE", "/api/v1/course/homework/{homework_id}"),
    ("GET", "/api/v1/tutor/settings"),
    ("PUT", "/api/v1/tutor/settings"),
    ("POST", "/api/v1/tutor/codex-login"),
    ("POST", "/api/v1/tutor/translate"),
    ("POST", "/api/v1/tutor/translate-question"),
    ("GET", "/api/v1/tutor/translation-history"),
    ("DELETE", "/api/v1/tutor/translation-history"),
    ("DELETE", "/api/v1/tutor/translation-history/{history_id}"),
    ("POST", "/api/v1/tutor/module1-chat"),
}


def test_course_and_tutor_public_route_surface_is_stable():
    paths = app.openapi()["paths"]
    actual = {
        (method.upper(), path)
        for path, operations in paths.items()
        if path.startswith(("/api/v1/course", "/api/v1/tutor"))
        and not path.startswith("/api/v1/course/backup")
        for method in operations
    }

    assert actual == EXPECTED_COURSE_AND_TUTOR_ROUTES


def test_named_success_response_schemas_are_stable():
    schema = app.openapi()
    expected = {
        ("/api/v1/course/state", "get"): "CourseStateResponse",
        ("/api/v1/course/state", "put"): "CourseStateResponse",
        ("/api/v1/course/exercises", "post"): "CourseExerciseResponse",
        ("/api/v1/course/exercises/{exercise_id}/answer", "post"): "CourseExerciseAttemptResponse",
        ("/api/v1/course/readings", "post"): "CourseReadingResponse",
        ("/api/v1/course/readings/{reading_id}/check", "post"): "CourseReadingAttemptResponse",
        ("/api/v1/course/vocabulary/{item_id}/review", "post"): "CourseVocabularyResponse",
        ("/api/v1/course/homework", "post"): "CourseHomeworkResponse",
        ("/api/v1/course/homework/{homework_id}/submit", "post"): "CourseHomeworkAttemptResponse",
        ("/api/v1/tutor/settings", "get"): "TutorSettingsResponse",
        ("/api/v1/tutor/settings", "put"): "TutorSettingsResponse",
        ("/api/v1/tutor/codex-login", "post"): "CodexLoginResponse",
        ("/api/v1/tutor/translate", "post"): "TutorTranslationResponse",
        ("/api/v1/tutor/translate-question", "post"): "TutorTranslationQuestionResponse",
        ("/api/v1/tutor/module1-chat", "post"): "TutorChatResponse",
    }

    actual = {
        key: schema["paths"][key[0]][key[1]]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].rsplit("/", 1)[-1]
        for key in expected
    }
    assert actual == expected
