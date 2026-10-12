from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ChallengeItem(BaseModel):
    id: int
    title: str
    challenge_type: str  # daily, weekly
    skill_category: str
    description: str
    hints: List[str]
    xp_reward: int
    solution_type: str
    is_completed: bool = False

    class Config:
        from_attributes = True


class ChallengeSubmitRequest(BaseModel):
    submission_text: str


class ChallengeSubmitResponse(BaseModel):
    is_valid: bool
    message: str
    xp_awarded: int
    total_user_xp: int


class BadgeItem(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    unlocked_at: Optional[str] = None


class RewardsProfileResponse(BaseModel):
    total_xp: int
    current_level: int
    level_title: str
    next_level_xp: int
    level_progress_percentage: float
    current_streak_days: int
    longest_streak_days: int
    weekly_activity: List[Dict[str, Any]]  # day, date, active, xp
    recent_badges: List[BadgeItem]
    next_milestone: str
