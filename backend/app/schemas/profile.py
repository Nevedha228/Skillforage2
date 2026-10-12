from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field

class ProfileUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=4)
    degree: Optional[str] = Field(None, min_length=2, max_length=100)
    branch: Optional[str] = Field(None, min_length=2, max_length=100)
    target_role: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=100)
    daily_study_hours: Optional[float] = Field(None, ge=0.5, le=16.0)
    learning_style: Optional[str] = Field(None, max_length=100)
    notifications_enabled: Optional[bool] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class DeleteAccountRequest(BaseModel):
    password: str


class DataExportResponse(BaseModel):
    user_profile: Dict[str, Any]
    assessments: List[Dict[str, Any]]
    roadmaps: List[Dict[str, Any]]
    learning_progress: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    challenges: List[Dict[str, Any]]
    xp_history: List[Dict[str, Any]]
    interviews: List[Dict[str, Any]]
    resume: Optional[Dict[str, Any]] = None
    skill_verifications: List[Dict[str, Any]]
