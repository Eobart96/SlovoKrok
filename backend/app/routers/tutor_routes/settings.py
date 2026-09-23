from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.tutor import CodexLoginResponse, TutorSettingsResponse, TutorSettingsUpdate
from app.services.tutor_settings import update_tutor_settings
from app.tutor import get_codex_connection_status, start_codex_login


router = APIRouter()


def _settings_response() -> TutorSettingsResponse:
    settings = get_settings()
    codex = get_codex_connection_status(settings)
    return TutorSettingsResponse(
        provider=settings.tutor_provider,
        codex_installed=codex.installed,
        codex_authenticated=codex.authenticated,
        codex_message=codex.message,
        openai_api_key_configured=bool(settings.openai_api_key),
        openai_model=settings.openai_model,
        polza_api_key_configured=bool(settings.polza_api_key),
        polza_model=settings.polza_model,
        polza_base_url=settings.polza_base_url,
    )


@router.get("/api/v1/tutor/settings", response_model=TutorSettingsResponse)
def get_tutor_settings() -> TutorSettingsResponse:
    return _settings_response()


@router.put("/api/v1/tutor/settings", response_model=TutorSettingsResponse)
def put_tutor_settings(request: TutorSettingsUpdate) -> TutorSettingsResponse:
    try:
        update_tutor_settings(get_settings(), request)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return _settings_response()


@router.post("/api/v1/tutor/codex-login", response_model=CodexLoginResponse)
def codex_login() -> CodexLoginResponse:
    try:
        status = start_codex_login(get_settings())
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return CodexLoginResponse(installed=status.installed, authenticated=status.authenticated, message=status.message)
