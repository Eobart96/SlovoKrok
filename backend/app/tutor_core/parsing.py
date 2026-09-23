import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.tutor_core.contracts import (
    AIResponseError,
    HomeworkGeneration,
    MAX_AI_RESPONSE_CHARS,
    TutorAssessment,
    TutorTranslation,
    TutorTranslationQuestion,
)
from app.tutor_core.exercise import GeneratedExercise


AIModelT = TypeVar("AIModelT", bound=BaseModel)


def parse_ai_json(
    response: str,
    model: type[AIModelT],
    *,
    allow_embedded_object: bool = False,
) -> AIModelT:
    """Parse bounded JSON from an untrusted provider into a strict model."""
    if not isinstance(response, str) or len(response) > MAX_AI_RESPONSE_CHARS:
        raise AIResponseError("AI response exceeds the allowed size")
    content = response.strip()
    if content.startswith("```"):
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    if allow_embedded_object and not content.startswith("{") and "{" in content and "}" in content:
        content = content[content.find("{"):content.rfind("}") + 1]
    try:
        payload = json.loads(content)
        if not isinstance(payload, dict):
            raise TypeError("AI response must be a JSON object")
        return model.model_validate(payload)
    except (json.JSONDecodeError, TypeError, ValidationError) as error:
        raise AIResponseError("AI response does not match the required schema") from error


def parse_tutor_translation(response: str) -> TutorTranslation:
    return parse_ai_json(response, TutorTranslation, allow_embedded_object=True)


def parse_tutor_translation_question(response: str) -> TutorTranslationQuestion:
    return parse_ai_json(response, TutorTranslationQuestion, allow_embedded_object=True)


def parse_tutor_assessment(response: str) -> TutorAssessment:
    """Validate a provider response and tolerate a markdown JSON fence."""
    return parse_ai_json(response, TutorAssessment)


def parse_homework_generation(response: str) -> HomeworkGeneration:
    return parse_ai_json(response, HomeworkGeneration)


def parse_generated_exercise(response: str) -> GeneratedExercise:
    return parse_ai_json(response, GeneratedExercise)
