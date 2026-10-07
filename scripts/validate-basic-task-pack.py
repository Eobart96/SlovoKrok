"""Validate the distributable task pack without touching user data or calling AI."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# app.database normally loads runtime settings and prepares legacy data.
# This standalone validator must bypass that path before importing it.
import app.config as isolated_config
isolated_config.get_settings = lambda: SimpleNamespace(database_url="sqlite://", runtime_data_dir=ROOT / "tmp/basic-task-pack/isolated-runtime", project_root=ROOT / "tmp/basic-task-pack/empty-project")

from app.database import Base
from app.routers.course_routes.materials import import_materials
from app.schemas.course import CourseMaterialCollection
from app.tutor_core.exercise import GeneratedExercise, assess_exercise_offline, decode_exercise_snapshot


def main():
    source = ROOT / "frontend/public/task-packs/slovokrok-a1-basic-v1.json"
    if source.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("Pack exceeds frontend import limit")
    raw = json.loads(source.read_text(encoding="utf-8"))
    pack = CourseMaterialCollection.model_validate(raw)
    roster = set()
    for name in ["texts-1-4.json", "texts-5-8.json"]:
        roster.update(json.loads((ROOT / "course-content/basic-task-pack" / name).read_text(encoding="utf-8")))
    if len(roster) != 83:
        raise ValueError("Expected 83 course topics")
    for rows, per_topic in [(pack.exercises, 20), (pack.readings, 2), (pack.homework, 2)]:
        counts = Counter(row.lesson_slug for row in rows)
        if counts != Counter({slug: per_topic for slug in roster}):
            raise ValueError("Wrong per-topic counts or lesson identifiers")
        if len({row.model_dump_json(exclude={"created_at"}) for row in rows}) != len(rows):
            raise ValueError("Duplicate tasks")
    formats = Counter()
    for exercise in pack.exercises:
        theory, interaction = decode_exercise_snapshot(exercise.theory_snapshot)
        if not theory:
            raise ValueError("Missing exercise snapshot")
        GeneratedExercise.model_validate({"question": exercise.question, "instruction": exercise.instruction, **interaction.model_dump()})
        expected = "; ".join(f"{pair.prompt} → {pair.answer}" for pair in interaction.pairs) if interaction.interaction_type == "match" else interaction.accepted_answers[0]
        result = assess_exercise_offline(interaction=interaction, answer=expected)
        if not result.is_correct or result.score != 100:
            raise ValueError(f"Saved reference does not pass its own assessment: {exercise.lesson_slug}: {exercise.question}: {result}")
        formats[interaction.interaction_type] += 1
    for reading in pack.readings:
        if not reading.reference_answer or reading.text.strip() == reading.reference_answer.strip():
            raise ValueError("Missing reading meaning reference")
    for homework in pack.homework:
        if not homework.reference_answer:
            raise ValueError("Missing homework reference")
    # Stable lesson identifiers can contain English "it" (who-what-is-it).
    # Scan learner content, not those compatibility identifiers.
    def content_strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                yield from content_strings(item)
        elif isinstance(value, dict):
            for key, item in value.items():
                if key != "lesson_slug":
                    yield from content_strings(item)
    serialized = "\n".join(content_strings(raw))
    if re.search(r"(?<!\w)(?:Boris|Marina|Марина|Horváth|Nováková|Novák|Ari|Ари|Eva|Peter|Martin|Lucia|Anna|Jana|Ján|Katka|Mária|Tomáš|Zuzana|Andrej|Michal|Juraj|Lukáš|Adam|Nina|Ema|Marek|Ivan|Адам|Нина|Мария|Иван|Алексей|IT|ИТ)(?!\w)|[\w.+-]+@[\w.-]+\.[a-z]{2,}|\+421[\d\s-]{6,}", serialized, re.I):
        raise ValueError("Personal identity or contact detected")
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            first = import_materials(pack, session)
            second = import_materials(pack, session)
            if (first.exercises.imported, first.readings.imported, first.homework.imported) != (1660, 166, 166):
                raise ValueError("Import counts mismatch")
            if any(bucket.imported for bucket in (second.exercises, second.readings, second.homework)):
                raise ValueError("Repeated import created duplicates")
    finally:
        engine.dispose()
    print(f"BASIC_TASK_PACK_OK topics=83 exercises=1660 readings=166 homework=166 bytes={source.stat().st_size}")
    print(f"formats={dict(formats)} import=1992 repeated_import=0 user_database=untouched")


if __name__ == "__main__":
    main()
