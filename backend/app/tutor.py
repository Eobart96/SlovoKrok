"""Stable compatibility facade for tutor contracts and provider adapters."""

from app.tutor_core.contracts import (
    AI_INVALID_RESPONSE_DETAIL,
    AI_PROVIDER_TIMEOUT_DETAIL,
    AI_PROVIDER_UNAVAILABLE_DETAIL,
    MAX_AI_RESPONSE_BYTES,
    MAX_AI_RESPONSE_CHARS,
    AIResponseError,
    HomeworkGeneration,
    StrictAIModel,
    TutorAssessment,
    TutorContext,
    TutorProvider,
    TutorProviderError,
    TutorProviderTimeout,
    TutorTranslation,
    TutorTranslationQuestion,
    VocabularyWord,
)
from app.tutor_core.exercise import (
    ExerciseInteraction,
    GeneratedExercise,
    GeneratedExercisePair,
    assess_exercise_offline,
    decode_exercise_snapshot,
    encode_exercise_snapshot,
    requested_exercise_interaction,
)
from app.tutor_core.parsing import (
    parse_ai_json,
    parse_generated_exercise,
    parse_homework_generation,
    parse_tutor_assessment,
    parse_tutor_translation,
    parse_tutor_translation_question,
)
from app.tutor_core.prompts import (
    build_exercise_chat_context,
    build_generated_exercise_context,
    build_mistake_chat_context,
    build_reading_check_context,
    build_reading_generation_context,
    build_translation_context,
    build_translation_question_context,
    build_tutor_context,
)
from app.tutor_providers.codex import (
    CodexCliProvider,
    CodexConnectionStatus,
    get_codex_connection_status,
    resolve_codex_executable,
    start_codex_login,
)
from app.tutor_providers.openai_compatible import OpenAIProvider


__all__ = [name for name in globals() if not name.startswith("_")]
