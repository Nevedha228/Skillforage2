from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class GenerateRoadmapRequest(BaseModel):
    target_role: Optional[str] = None
    weekly_hours: Optional[float] = Field(None, ge=2.0, le=40.0)
    learning_style: Optional[str] = None


class RoadmapTask(BaseModel):
    id: str
    title: str
    task_type: str  # lesson, exercise, project, checkpoint
    skill: str
    estimated_hours: float
    is_completed: bool = False
    completion_criteria: str
    resource_link: Optional[str] = None


class RoadmapPhase(BaseModel):
    phase_number: int
    title: str
    focus: str
    prerequisite_skills: List[str]
    tasks: List[RoadmapTask]
    milestone: str
    estimated_weeks: int


class RoadmapResponse(BaseModel):
    id: int
    target_role: str
    target_role_title: str
    version: int
    year_emphasis: str
    weekly_hours: float
    total_phases: int
    total_tasks: int
    completed_tasks_count: int
    progress_percentage: float
    phases: List[RoadmapPhase]
    missed_tasks_count: int
    rescheduling_suggestion: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class CompleteTaskRequest(BaseModel):
    task_id: str


class RescheduleRoadmapRequest(BaseModel):
    reason: Optional[str] = "Pacing adjustment"
    adjusted_weekly_hours: Optional[float] = None
