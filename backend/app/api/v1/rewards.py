from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.schemas.challenge import RewardsProfileResponse
from app.services.rewards_service import calculate_user_rewards

router = APIRouter(prefix="/rewards", tags=["Streaks & Rewards"])

@router.get("/profile", response_model=RewardsProfileResponse)
def get_user_rewards_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns verified gamification metrics:
    All scores and streaks derived entirely from persisted DB records.
    Never uses gambling mechanics; a missed day never erases previous history.
    """
    return calculate_user_rewards(current_user, db)
