from dataclasses import dataclass
from typing import Annotated, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator


MAX_AI_RESPONSE_CHARS = 32_000
MAX_AI_RESPONSE_BYTES = 128_000
AI_INVALID_RESPONSE_DETAIL = "ИИ вернул ответ в неверном формате"
AI_PROVIDER_UNAVAILABLE_DETAIL = "AI provider временно недоступен"
AI_PROVIDER_TIMEOUT_DETAIL = "AI provider не ответил вовремя"


class AIResponseError(ValueError):
    """Provider output cannot be trusted or validated."""


class TutorProviderError(RuntimeError):
    """A provider failed before returning a usable response."""


class TutorProviderTimeout(TutorProviderError):
    """A provider exceeded the configured request deadline."""


class StrictAIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)


@dataclass(frozen=True)
class TutorContext:
    prompt: str


class TutorProvider(Protocol):
    def respond(self, context: TutorContext) -> str:
        ...


class VocabularyWord(StrictAIModel):
    word: str = Field(min_length=1, max_length=120)
    translation: str = Field(min_length=1, max_length=240)
    example: str | None = Field(default=None, max_length=500)


class TutorAssessment(StrictAIModel):
    is_correct: bool
    score: int = Field(ge=0, le=100)
    corrected_answer: str = Field(min_length=1, max_length=2_000)
    explanation: str = Field(min_length=1, max_length=4_000)
    next_exercise: str = Field(min_length=1, max_length=2_000)
    mistake_category: str | None = Field(default=None, max_length=120)
    new_words: list[VocabularyWord] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def normalize_correct_score(self):
        if self.is_correct:
            self.score = 100
        return self


class HomeworkGeneration(StrictAIModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=4_000)
    focus_category: str = Field(min_length=1, max_length=200)


class TutorTranslation(StrictAIModel):
    translation: str = Field(min_length=1, max_length=4_000)
    alternatives: list[Annotated[str, Field(min_length=1, max_length=4_000)]] = Field(default_factory=list, max_length=2)
    note: str | None = Field(default=None, max_length=500)


class TutorTranslationQuestion(StrictAIModel):
    answer: str = Field(min_length=1, max_length=4_000)
