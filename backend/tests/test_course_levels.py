import pytest
from types import SimpleNamespace
import app.tutor_core.prompts as prompts

from app.routers.course_routes.common import course_level_for_slug
from app.tutor_core.prompts import build_generated_exercise_context, build_reading_generation_context
from app.dependencies import get_tutor_provider
from app.main import app


@pytest.mark.parametrize("slug,level", [("greetings", "A1"), ("course-progress", "A1"), ("a2-intro", "A2"), ("course:a2:progress", "A2"), ("module:a2-module-1", "A2"), ("section:a2-module-1:intro", "A2")])
def test_reading_checks_use_saved_reading_level_and_preserve_both_collections(client, slug, level):
    class ReadingProvider:
        def __init__(self):
            self.prompts = []

        def respond(self, context):
            self.prompts.append(context.prompt)
            if '"original_text"' in context.prompt:
                return '{"score":85,"feedback":"Главное понято, итог уточните.","corrected_retelling":"Анна представилась."}'
            return '{"title":"Знакомство","text":"Volám sa Anna.","instruction":"Перескажите.","reference_answer":"Анна представилась."}'

    provider = ReadingProvider()
    app.dependency_overrides[get_tutor_provider] = lambda: provider
    other = client.post("/api/v1/course/readings", json={"lesson_slug": "a2-other" if level == "A1" else "greetings", "lesson_title": "Other", "theory": "Theory", "completed_theory": "Words"})
    assert other.status_code == 200
    created = client.post("/api/v1/course/readings", json={"lesson_slug": slug, "lesson_title": "Topic", "theory": "Theory", "completed_theory": "Words"})
    assert created.status_code == 200
    checked = client.post(f"/api/v1/course/readings/{created.json()['id']}/check", json={"retelling": "Анна представилась.", "assessment_mode": "online"})
    assert checked.status_code == 200
    assert f"уровня {level}" in provider.prompts[-1]
    assert ("КРИТЕРИИ A2" in provider.prompts[-1]) == (level == "A2")
    assert ("ЧТЕНИЕ A2" in provider.prompts[-2]) == (level == "A2")
    assert len(client.get("/api/v1/course/readings").json()) == 2


@pytest.mark.parametrize("slug", ["a2-nominative-plural-things", "module:a2-module-2", "section:a2-module-2:plural", "course:a2:progress", "course:a2:mistakes"])
def test_a2_task_scopes_select_a2_prompt(slug):
    assert course_level_for_slug(slug) == "A2"


@pytest.mark.parametrize("slug", ["greetings", "course-progress", "course-mistakes", "module:module-2", "section:module-2:plural"])
def test_legacy_task_scopes_remain_a1(slug):
    assert course_level_for_slug(slug) == "A1"


def test_generation_prompts_use_selected_level_with_a1_default():
    assert "языку A1" in build_generated_exercise_context(lesson_title="Topic", theory="Theory").prompt
    assert "языку A2" in build_generated_exercise_context(lesson_title="Topic", theory="Theory", level="A2").prompt
    assert "языка A2" in build_reading_generation_context(lesson_title="Topic", theory="Theory", completed_theory="Words", level="A2").prompt


def test_a2_teacher_context_does_not_load_a1_roadmap_or_method(tmp_path, monkeypatch):
    read_names = []
    def read(path):
        read_names.append(path.name)
        return "Profile"
    monkeypatch.setattr(prompts, "_read_learning_file", read)
    settings = SimpleNamespace(learning_path=tmp_path, project_root=tmp_path, share_private_tutor_profile=False)
    context = prompts.build_tutor_context(settings, "Задание A2", course_level="A2")
    assert read_names == ["student_profile.md"]
    assert "Задание A2" in context.prompt
    assert "Не ограничивай A2 дорожной картой A1" in context.prompt
