from fastapi import APIRouter
from app.services.learner_profile import LearnerProfile, read_profile, write_profile

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("", response_model=LearnerProfile)
def get_profile():
    return read_profile()


@router.put("", response_model=LearnerProfile)
def save_profile(profile: LearnerProfile):
    return write_profile(profile)
