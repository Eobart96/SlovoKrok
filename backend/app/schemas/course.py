from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator


LessonStep = Annotated[int, Field(ge=0, le=10_000, strict=True)]


class PersonalCheatSheetPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=4_000)
    createdAt: datetime
    updatedAt: datetime

    @model_validator(mode="after")
    def validate_timestamps(self):
        if (self.createdAt.utcoffset() is None) != (self.updatedAt.utcoffset() is None):
            raise ValueError("Cheat sheet timestamps use different timezone modes")
        if self.updatedAt < self.createdAt:
            raise ValueError("Cheat sheet update precedes creation")
        return self


class CourseMistakeReviewTaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=4_000)
    learnerAnswer: str = Field(max_length=4_000)
    explanation: str = Field(max_length=4_000)
    kind: Literal["exact", "open"]


class CourseMistakeCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=4_000)
    expected_answer: str = Field(min_length=1, max_length=2_000)
    accepted_answers: list[Annotated[str, Field(min_length=1, max_length=2_000)]] = Field(default_factory=list, max_length=20)
    answer: str = Field(min_length=1, max_length=4_000)
    kind: Literal["exact", "open"]
    source_exercise_id: int | None = Field(default=None, gt=0)
    assessment_mode: Literal["online", "offline"] = "online"


class CourseMistakePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=160)
    lessonSlug: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=2_000)
    answer: str = Field(min_length=1, max_length=2_000)
    attempts: int = Field(ge=0, le=100_000, strict=True)
    mastered: bool = Field(strict=True)
    reviewStage: int | None = Field(default=None, ge=0, le=2, strict=True)
    dueAt: datetime | None = None
    reviewTask: CourseMistakeReviewTaskPayload | None = None


class CourseChatMessagePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(ge=0, strict=True)
    role: Literal["assistant", "user"]
    text: str = Field(min_length=1, max_length=4_000)
    task: str | None = Field(default=None, max_length=2_000)
    suggestions: list[str] | None = Field(default=None, max_length=3)
    countsAsPractice: bool | None = Field(default=None, strict=True)
    createdAt: datetime | None = None
    interactionKind: Literal["answer", "clarification", "continue"] | None = None
    diagnostic: dict[str, str | int | float | bool | None] | None = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def validate_suggestions(self):
        if self.suggestions is not None and any(not 1 <= len(value) <= 160 for value in self.suggestions):
            raise ValueError("Invalid chat suggestion")
        if self.diagnostic is not None and any(isinstance(value, str) and len(value) > 2_000 for value in self.diagnostic.values()):
            raise ValueError("Diagnostic text is too long")
        return self


class CourseSummaryEvidencePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    coreCorrect: int = Field(ge=0, le=10_000, strict=True)
    coreTotal: int = Field(ge=0, le=10_000, strict=True)

    @model_validator(mode="after")
    def validate_score(self):
        if self.coreCorrect > self.coreTotal:
            raise ValueError("Correct evidence exceeds total")
        return self


class CourseLessonSummaryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    understanding: int = Field(ge=0, le=100, strict=True)
    level: str = Field(min_length=1, max_length=120)
    strengths: list[str] = Field(max_length=10)
    mistakes: list[str] | None = Field(default=None, max_length=20)
    review: list[str] = Field(max_length=10)
    userTurns: int = Field(ge=0, le=10_000, strict=True)
    evidence: CourseSummaryEvidencePayload | None = None

    @model_validator(mode="after")
    def validate_text_lists(self):
        values = [*self.strengths, *self.review, *(self.mistakes or [])]
        if any(not 1 <= len(value) <= 2_000 for value in values):
            raise ValueError("Invalid lesson summary text")
        return self


class CoursePositionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    activeModule: int = Field(ge=1, le=8, strict=True)
    selectedSlug: str = Field(min_length=1, max_length=100)


class CourseStatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activeLevel: Literal["A1", "A2"] = "A1"
    levelPositions: dict[Literal["A1", "A2"], CoursePositionPayload] = Field(default_factory=dict, max_length=2)
    activeModule: int = Field(default=1, ge=1, le=8, strict=True)
    selectedSlug: str | None = Field(default=None, min_length=1, max_length=100)
    fontSize: Literal["normal", "large", "extra-large"] = "large"
    progress: dict[str, Literal["not_started", "in_progress", "completed"]] = Field(default_factory=dict, max_length=500)
    lessonSteps: dict[str, LessonStep] = Field(default_factory=dict, max_length=500)
    checkSelections: dict[str, str] = Field(default_factory=dict, max_length=5_000)
    practiceAnswers: dict[str, str] = Field(default_factory=dict, max_length=5_000)
    practiceResults: dict[str, StrictBool] = Field(default_factory=dict, max_length=5_000)
    mistakes: dict[str, CourseMistakePayload] = Field(default_factory=dict, max_length=5_000)
    finalSelections: dict[str, str] = Field(default_factory=dict, max_length=1_000)
    finalCompleted: bool = Field(default=False, strict=True)
    finalCompletedModules: dict[str, StrictBool] = Field(default_factory=dict, max_length=20)
    chatHistories: dict[str, list[CourseChatMessagePayload]] = Field(default_factory=dict, max_length=500)
    lessonSummaries: dict[str, CourseLessonSummaryPayload] = Field(default_factory=dict, max_length=500)
    personalCheatSheets: list[PersonalCheatSheetPayload] = Field(default_factory=list, max_length=200)

    @model_validator(mode="after")
    def validate_nested_bounds(self):
        mappings = (
            self.progress,
            self.lessonSteps,
            self.checkSelections,
            self.practiceAnswers,
            self.practiceResults,
            self.mistakes,
            self.finalSelections,
            self.chatHistories,
            self.lessonSummaries,
        )
        if any(not 1 <= len(key) <= 160 for mapping in mappings for key in mapping):
            raise ValueError("Invalid course state key")
        valid_module_keys = {
            key
            for module in range(1, 9)
            for key in (str(module), f"a1:{module}", f"a2:{module}")
        }
        if any(key not in valid_module_keys for key in self.finalCompletedModules):
            raise ValueError("Invalid completed module identifier")
        if any(len(value) > 2_000 for mapping in (self.checkSelections, self.practiceAnswers, self.finalSelections) for value in mapping.values()):
            raise ValueError("Saved answer is too long")
        if any(len(messages) > 500 for messages in self.chatHistories.values()):
            raise ValueError("Too many chat messages")
        return self


class CourseStateResponse(BaseModel):
    exists: bool
    schema_version: int = 3
    revision: str | None = Field(default=None, pattern="^[0-9a-f]{64}$")
    state: CourseStatePayload | None = None
    updated_at: datetime | None = None


class CourseExerciseGenerateRequest(BaseModel):
    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    theory: str = Field(min_length=1, max_length=12_000)


class CourseExerciseAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=4_000)
    assessment_mode: Literal["online", "offline"] = "online"


class _ConsistentScoredAttempt(BaseModel):
    is_correct: bool
    score: int

    @model_validator(mode="after")
    def normalize_correct_score(self):
        if self.is_correct:
            self.score = 100
        return self


class CourseExerciseAttemptResponse(_ConsistentScoredAttempt):
    id: int
    answer: str
    corrected_answer: str
    explanation: str
    next_exercise: str
    created_at: datetime


class CourseExerciseResponse(BaseModel):
    id: int
    lesson_slug: str
    lesson_title: str
    question: str
    instruction: str
    interaction_type: Literal["text", "choice", "order", "match"] = "text"
    options: list[str] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    pair_prompts: list[str] = Field(default_factory=list)
    pair_options: list[str] = Field(default_factory=list)
    created_at: datetime
    latest_attempt: CourseExerciseAttemptResponse | None = None


class _CourseBatchGenerateRequest(BaseModel):
    batch_index: int = Field(default=1, ge=1, le=20)
    batch_total: int = Field(default=1, ge=1, le=20)

    @model_validator(mode="after")
    def validate_batch_position(self):
        if self.batch_index > self.batch_total:
            raise ValueError("Batch index exceeds batch total")
        return self


class CourseReadingGenerateRequest(_CourseBatchGenerateRequest):
    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    theory: str = Field(min_length=1, max_length=12_000)
    completed_theory: str = Field(default="", max_length=30_000)


class CourseReadingCheckRequest(BaseModel):
    retelling: str = Field(min_length=1, max_length=4_000)
    assessment_mode: Literal["online", "offline"] = "online"


class CourseReadingCheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    score: int = Field(ge=0, le=100)
    feedback: str = Field(min_length=1, max_length=4_000)
    corrected_retelling: str = Field(min_length=1, max_length=4_000)


class CourseReadingAttemptResponse(BaseModel):
    id: int
    retelling: str
    score: int
    feedback: str
    corrected_retelling: str
    created_at: datetime


class CourseReadingResponse(BaseModel):
    id: int
    lesson_slug: str
    lesson_title: str
    title: str
    text: str
    instruction: str
    created_at: datetime
    offline_ready: bool = False
    latest_attempt: CourseReadingAttemptResponse | None = None


class CourseVocabularySeedItem(BaseModel):
    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    word: str = Field(min_length=1, max_length=255)
    translation: str = Field(min_length=1, max_length=500)
    example: str | None = Field(default=None, max_length=2_000)


class CourseVocabularySyncRequest(BaseModel):
    items: list[CourseVocabularySeedItem] = Field(max_length=500)


class CourseVocabularyResponse(BaseModel):
    id: int
    lesson_slug: str
    lesson_title: str
    word: str
    translation: str
    example: str | None
    review_count: int
    interval_days: int
    next_review_at: datetime | None
    is_due: bool


class CourseHomeworkGenerateRequest(_CourseBatchGenerateRequest):
    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    theory: str = Field(min_length=1, max_length=12_000)
    known_mistakes: list[str] = Field(default_factory=list, max_length=20)


class CourseHomeworkSubmitRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=4_000)
    assessment_mode: Literal["online", "offline"] = "online"


class CourseHomeworkAttemptResponse(_ConsistentScoredAttempt):
    id: int
    answer: str
    corrected_answer: str
    explanation: str
    next_exercise: str
    created_at: datetime


class CourseHomeworkResponse(BaseModel):
    id: int
    lesson_slug: str
    lesson_title: str
    title: str
    description: str
    focus_category: str
    created_at: datetime
    offline_ready: bool = False
    latest_attempt: CourseHomeworkAttemptResponse | None = None


class CourseMaterialExerciseItem(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    question: str = Field(min_length=1, max_length=8_000)
    instruction: str = Field(min_length=1, max_length=4_000)
    theory_snapshot: str = Field(min_length=1, max_length=100_000)
    created_at: datetime


class CourseMaterialReadingItem(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    text: str = Field(min_length=1, max_length=8_000)
    instruction: str = Field(min_length=1, max_length=1_000)
    reference_answer: str | None = Field(default=None, max_length=4_000)
    created_at: datetime


class CourseMaterialHomeworkItem(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lesson_slug: str = Field(min_length=1, max_length=100)
    lesson_title: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=8_000)
    focus_category: str = Field(min_length=1, max_length=255)
    theory_snapshot: str = Field(min_length=1, max_length=12_000)
    reference_answer: str | None = Field(default=None, max_length=4_000)
    created_at: datetime


class CourseMaterialCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    format: Literal["slovokrok-course-materials"]
    version: Literal[1]
    exported_at: datetime
    exercises: list[CourseMaterialExerciseItem] = Field(max_length=2_000)
    readings: list[CourseMaterialReadingItem] = Field(max_length=2_000)
    homework: list[CourseMaterialHomeworkItem] = Field(max_length=2_000)


class CourseMaterialImportBucket(BaseModel):
    imported: int = Field(ge=0)
    skipped: int = Field(ge=0)
    total: int = Field(ge=0)


class CourseMaterialImportResponse(BaseModel):
    exercises: CourseMaterialImportBucket
    readings: CourseMaterialImportBucket
    homework: CourseMaterialImportBucket


class CourseTasksDeleteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmation: Literal["delete-all-course-tasks"]


class CourseTasksDeleteResponse(BaseModel):
    deleted: Literal[True]
    exercises_deleted: int = Field(ge=0)
    exercise_attempts_deleted: int = Field(ge=0)
    readings_deleted: int = Field(ge=0)
    reading_attempts_deleted: int = Field(ge=0)
    homework_deleted: int = Field(ge=0)
    homework_attempts_deleted: int = Field(ge=0)
