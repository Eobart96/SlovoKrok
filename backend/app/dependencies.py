from fastapi import HTTPException

from app.config import get_settings
from app.tutor import CodexCliProvider, OpenAIProvider, TutorProvider
from app.services.learner_profile import personalize_context


class ProfileTutorProvider:
    def __init__(self, provider):
        self.provider = provider

    def respond(self, context):
        return self.provider.respond(personalize_context(context))


def get_tutor_provider() -> TutorProvider:
    """Select the configured AI provider for routes that need a tutor."""
    settings = get_settings()
    if settings.tutor_provider == "openai":
        if not settings.openai_api_key:
            raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
        return ProfileTutorProvider(OpenAIProvider(settings))
    if settings.tutor_provider == "polza":
        if not settings.polza_api_key:
            raise HTTPException(status_code=503, detail="POLZA_API_KEY is not configured")
        return ProfileTutorProvider(OpenAIProvider(
            settings,
            api_key=settings.polza_api_key,
            model=settings.polza_model,
            base_url=settings.polza_base_url,
            use_chat_completions=True,
        ))
    if settings.tutor_provider == "codex":
        return ProfileTutorProvider(CodexCliProvider(settings))
    raise HTTPException(status_code=500, detail="Unsupported TUTOR_PROVIDER")
