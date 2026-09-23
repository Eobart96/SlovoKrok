from fastapi import APIRouter

from app.routers.course_routes import exercises, homework, readings, state, vocabulary


router = APIRouter(prefix="/api/v1/course", tags=["course"])
router.include_router(state.router)
router.include_router(exercises.router)
router.include_router(readings.router)
router.include_router(vocabulary.router)
router.include_router(homework.router)
