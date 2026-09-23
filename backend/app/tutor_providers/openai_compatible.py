from app.config import Settings
from app.tutor_core.contracts import (
    MAX_AI_RESPONSE_CHARS,
    AIResponseError,
    TutorContext,
    TutorProviderError,
    TutorProviderTimeout,
)


class OpenAIProvider:
    """Optional API provider using the same TutorContext as Codex mode."""

    def __init__(
        self,
        settings: Settings,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.settings = settings
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.base_url = base_url

    def respond(self, context: TutorContext) -> str:
        from openai import APIConnectionError, APIStatusError, APITimeoutError, InternalServerError, OpenAI, RateLimitError

        client_kwargs = {
            "api_key": self.api_key,
            "timeout": float(self.settings.tutor_timeout_seconds),
            "max_retries": 1,
        }
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        client = OpenAI(**client_kwargs)
        try:
            response = client.responses.create(model=self.model, input=context.prompt)
        except APITimeoutError as error:
            raise TutorProviderTimeout("OpenAI-compatible provider timed out") from error
        except (APIConnectionError, RateLimitError, InternalServerError, APIStatusError) as error:
            raise TutorProviderError("OpenAI-compatible provider request failed") from error
        output = response.output_text
        if not isinstance(output, str) or not output.strip():
            raise AIResponseError("Provider returned an empty response")
        if len(output) > MAX_AI_RESPONSE_CHARS:
            raise AIResponseError("Provider response exceeds the allowed size")
        return output
