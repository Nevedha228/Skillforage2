from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EmergencySprintRequest(BaseModel):
    target_role: str
    days_left: int = Field(14, ge=3, le=60)  # 7, 14, 30, custom
    hours_per_day: float = Field(3.0, ge=1.0, le=12.0)
    current_level: str = "Developing"  # Foundational, Developing, Competent
    interview_type: str = "technical"  # technical, full_loop, hr
    weak_areas: List[str] = Field(default_factory=list)


class SprintDayPlan(BaseModel):
    day_number: int
    focus_topic: str
    time_allocation_hours: float
    checklist: List[str]
    practice_tasks: List[str]
    milestone_check: Optional[str] = None


class EmergencySprintResponse(BaseModel):
    target_role: str
    duration_days: int
    total_dedicated_hours: float
    readiness_target_score: int
    daily_schedule: List[SprintDayPlan]
    critical_checkpoints: List[Dict[str, Any]]
    guidance_message: str
