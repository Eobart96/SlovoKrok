from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.course import router as course_router
from app.routers.backup import router as backup_router
from app.routers.system import router as system_router
from app.routers.tutor import router as tutor_router
from app.routers.reports import router as reports_router
from app.routers.profile import router as profile_router
from app.services.startup import initialize_application


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_application()
    yield


app = FastAPI(title=get_settings().app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tutor_router)
app.include_router(course_router)
app.include_router(backup_router)
app.include_router(system_router)
app.include_router(reports_router)
app.include_router(profile_router)
