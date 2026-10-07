from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ShortChatSuggestion = Annotated[str, Field(min_length=1, max_length=160)]


class TutorChatHistoryMessage(BaseModel):
    role: str
    content: str = Field(max_length=2_000)


class TutorChatRequest(BaseModel):
    lesson_slug: str = Field(max_length=100)
    lesson_title: str = Field(max_length=200)
    goals: list[str] = Field(max_length=10)
    theory: str = Field(max_length=8_000)
    known_mistakes: list[str] = Field(default_factory=list, max_length=20)
    history: list[TutorChatHistoryMessage] = Field(default_factory=list, max_length=6)
    message: str = Field(min_length=1, max_length=2_000)
    current_task: str | None = Field(default=None, max_length=500)
    interaction_kind: Literal["answer", "clarification", "continue"] = "answer"
    is_final_turn: bool = False


class TutorChatOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    reply: str = Field(min_length=1, max_length=4_000)
    correction: str | None = Field(default=None, max_length=2_000)
    explanation: str | None = Field(default=None, max_length=4_000)
    next_question: str | None = Field(default=None, max_length=500)
    suggestions: list[ShortChatSuggestion] = Field(default_factory=list, max_length=3)
    mistake_original: str | None = Field(default=None, max_length=2_000)
    mistake_corrected: str | None = Field(default=None, max_length=2_000)

    @model_validator(mode="after")
    def validate_suggestions_match_question(self):
        if self.next_question is None and self.suggestions:
            raise ValueError("Suggestions require a next question")
        if self.next_question is not None and not 2 <= len(self.suggestions) <= 3:
            raise ValueError("A next question requires 2-3 suggestions")
        return self


class TutorChatResponse(TutorChatOutput):
    provider: str = Field(min_length=1, max_length=40)


TranslationDirection = Literal["ru-sk", "sk-ru"]
TranslationAlternative = Annotated[str, Field(min_length=1, max_length=4_000)]


class TutorTranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)
    direction: TranslationDirection


class TutorTranslationResponse(BaseModel):
    history_id: int
    provider: str
    translation: str = Field(min_length=1, max_length=4_000)
    alternatives: list[TranslationAlternative] = Field(default_factory=list, max_length=2)
    note: str | None = Field(default=None, max_length=500)


class TutorTranslationQuestionRequest(BaseModel):
    history_id: int | None = Field(default=None, ge=1)
    source_text: str = Field(min_length=1, max_length=2_000)
    translation: str = Field(min_length=1, max_length=4_000)
    direction: TranslationDirection
    question: str = Field(min_length=1, max_length=1_000)


class TutorTranslationQuestionResponse(BaseModel):
    history_id: int
    provider: str
    answer: str = Field(min_length=1, max_length=4_000)


class TutorTranslationHistoryQuestionResponse(BaseModel):
    id: int
    question: str
    answer: str
    provider: str
    created_at: datetime


class TutorTranslationHistoryResponse(BaseModel):
    id: int
    direction: TranslationDirection
    source_text: str
    translation: str
    alternatives: list[TranslationAlternative] = Field(default_factory=list, max_length=2)
    note: str | None = None
    provider: str
    created_at: datetime
    questions: list[TutorTranslationHistoryQuestionResponse] = Field(default_factory=list)


class TutorTranslationHistoryClearRequest(BaseModel):
    confirmation: Literal["delete-translation-history"]


TutorProviderName = Literal["codex", "openai", "polza"]


class TutorSettingsResponse(BaseModel):
    provider: TutorProviderName
    codex_installed: bool
    codex_authenticated: bool
    codex_message: str
    openai_api_key_configured: bool
    openai_model: str
    polza_api_key_configured: bool
    polza_model: str
    polza_base_url: str


class TutorSettingsUpdate(BaseModel):
    provider: TutorProviderName
    openai_api_key: str | None = Field(default=None, max_length=512)
    openai_model: str = Field(default="gpt-5", min_length=1, max_length=120)
    polza_api_key: str | None = Field(default=None, max_length=512)
    polza_model: str = Field(default="google/gemini-2.5-flash-lite", min_length=1, max_length=160)
    clear_openai_api_key: bool = False
    clear_polza_api_key: bool = False


class CodexLoginResponse(BaseModel):
    installed: bool
    authenticated: bool
    message: str
