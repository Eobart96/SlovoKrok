from fastapi import APIRouter

from app.routers.tutor_routes import chat, settings, translations


router = APIRouter(tags=["tutor"])
router.include_router(settings.router)
router.include_router(translations.router)
router.include_router(chat.router)
