from collections import Counter
import json
import re
from typing import Annotated, Literal
import unicodedata

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.tutor_core.contracts import StrictAIModel, TutorAssessment


def _normalized_exercise_answer(answer: str) -> str:
    normalized = unicodedata.normalize("NFKC", answer).casefold().strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s+([,.;:!?])", r"\1", normalized)
    return normalized.strip(" .!?…")


class GeneratedExercisePair(StrictAIModel):
    prompt: str = Field(min_length=1, max_length=200)
    answer: str = Field(min_length=1, max_length=200)


class ExerciseInteraction(BaseModel):
    interaction_type: Literal["text", "choice", "order", "match"] = "text"
    options: list[Annotated[str, Field(min_length=1, max_length=200)]] = Field(default_factory=list, max_length=6)
    tokens: list[Annotated[str, Field(min_length=1, max_length=100)]] = Field(default_factory=list, max_length=12)
    pairs: list[GeneratedExercisePair] = Field(default_factory=list, max_length=5)
    accepted_answers: list[Annotated[str, Field(min_length=1, max_length=500)]] = Field(default_factory=list, max_length=5)

    @model_validator(mode="after")
    def validate_interaction(self):
        if self.interaction_type == "choice" and not 2 <= len(self.options) <= 6:
            raise ValueError("Choice exercises require 2-6 options")
        if self.interaction_type == "order" and not 2 <= len(self.tokens) <= 12:
            raise ValueError("Order exercises require 2-12 tokens")
        if self.interaction_type == "match" and not 2 <= len(self.pairs) <= 5:
            raise ValueError("Matching exercises require 2-5 pairs")
        if self.interaction_type != "choice" and self.options:
            raise ValueError("Options are only valid for choice exercises")
        if self.interaction_type != "order" and self.tokens:
            raise ValueError("Tokens are only valid for order exercises")
        if self.interaction_type != "match" and self.pairs:
            raise ValueError("Pairs are only valid for matching exercises")
        if len(self.options) != len(set(self.options)):
            raise ValueError("Choice options must be unique")
        if len(self.accepted_answers) != len(set(self.accepted_answers)):
            raise ValueError("Accepted answers must be unique")
        if self.pairs and (len({pair.prompt for pair in self.pairs}) != len(self.pairs) or len({pair.answer for pair in self.pairs}) != len(self.pairs)):
            raise ValueError("Matching prompts and answers must be unique")
        return self


class GeneratedExercise(ExerciseInteraction):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)
    question: str = Field(min_length=1, max_length=2_000)
    instruction: str = Field(min_length=1, max_length=1_000)

    @model_validator(mode="after")
    def validate_reference_answer(self):
        if self.interaction_type == "match":
            if self.accepted_answers:
                raise ValueError("Matching exercises use pairs instead of accepted answers")
            return self
        if not self.accepted_answers:
            raise ValueError("Generated exercises require at least one accepted answer")
        if self.interaction_type == "choice" and any(_normalized_exercise_answer(answer) not in {_normalized_exercise_answer(option) for option in self.options} for answer in self.accepted_answers):
            raise ValueError("Every accepted choice answer must be one of the options")
        if self.interaction_type == "order":
            available_tokens = Counter(_normalized_exercise_answer(token) for token in self.tokens)
            if any(Counter(_normalized_exercise_answer(answer).split()) != available_tokens for answer in self.accepted_answers):
                raise ValueError("Every accepted order answer must use exactly the available tokens")
        return self


_EXERCISE_SNAPSHOT_PREFIX = "slovokrok-exercise:v1:"


def encode_exercise_snapshot(theory: str, exercise: GeneratedExercise) -> str:
    payload = {"theory": theory, **ExerciseInteraction.model_validate(exercise.model_dump()).model_dump()}
    return _EXERCISE_SNAPSHOT_PREFIX + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def decode_exercise_snapshot(snapshot: str) -> tuple[str, ExerciseInteraction]:
    if not snapshot.startswith(_EXERCISE_SNAPSHOT_PREFIX):
        return snapshot, ExerciseInteraction()
    try:
        payload = json.loads(snapshot.removeprefix(_EXERCISE_SNAPSHOT_PREFIX))
        theory = payload.pop("theory")
        if not isinstance(theory, str):
            raise ValueError("Invalid exercise theory")
        return theory, ExerciseInteraction.model_validate(payload)
    except (json.JSONDecodeError, TypeError, ValueError):
        return "", ExerciseInteraction()


def requested_exercise_interaction(theory: str) -> Literal["text", "choice", "order", "match"] | None:
    match = re.search(r"Тип интерактива:\s*(text|choice|order|match)\b", theory)
    return match.group(1) if match else None


def assess_exercise_offline(*, interaction: ExerciseInteraction, answer: str) -> TutorAssessment:
    """Check an exercise against its saved reference without an external provider."""
    if interaction.interaction_type == "match":
        expected_pairs = {pair.prompt: pair.answer for pair in interaction.pairs}
        submitted_pairs: dict[str, str] = {}
        for item in answer.split(";"):
            prompt, separator, selected = item.partition("→")
            if separator and prompt.strip() and selected.strip():
                submitted_pairs[_normalized_exercise_answer(prompt)] = _normalized_exercise_answer(selected)
        correct_count = sum(
            submitted_pairs.get(_normalized_exercise_answer(prompt)) == _normalized_exercise_answer(expected)
            for prompt, expected in expected_pairs.items()
        )
        is_correct = bool(expected_pairs) and correct_count == len(expected_pairs)
        score = round(correct_count / len(expected_pairs) * 100) if expected_pairs else 0
        corrected_answer = "; ".join(f"{prompt} → {expected}" for prompt, expected in expected_pairs.items())
    else:
        if not interaction.accepted_answers:
            raise ValueError("This saved exercise has no offline reference answer")
        normalized_answer = _normalized_exercise_answer(answer)
        is_correct = normalized_answer in {_normalized_exercise_answer(item) for item in interaction.accepted_answers}
        score = 100 if is_correct else 0
        corrected_answer = interaction.accepted_answers[0]
    return TutorAssessment(
        is_correct=is_correct,
        score=score,
        corrected_answer=corrected_answer,
        explanation="Ответ совпадает с сохранённым эталоном." if is_correct else "Ответ не совпал с сохранённым эталоном. Проверьте форму и порядок слов.",
        next_exercise="Переходите к следующему сохранённому заданию." if is_correct else "Исправьте ответ и попробуйте ещё раз.",
    )
