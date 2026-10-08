import pytest
from types import SimpleNamespace
import app.tutor_core.prompts as prompts

from app.routers.course_routes.common import course_level_for_slug
from app.tutor_core.prompts import build_generated_exercise_context, build_reading_generation_context


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
