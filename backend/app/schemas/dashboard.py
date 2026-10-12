from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class DashboardStats(BaseModel):
    is_empty_state: bool
    username: str
    year: int
    degree: str
    branch: str
    target_role: Optional[str] = None
    target_role_title: Optional[str] = None

    # Real persisted metrics
    total_assessments_taken: int
    average_assessment_score: float
    total_verified_skills: int
    roadmap_progress_percentage: float
    total_xp: int
    current_streak_days: int
    total_projects_count: int
    interviews_practiced_count: int

    # Guidance & recommendations
    onboarding_checklist: List[Dict[str, Any]]
    suggested_next_action: Dict[str, str]
    recent_activities: List[Dict[str, Any]]
