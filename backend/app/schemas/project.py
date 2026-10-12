from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re

class ProjectTemplateItem(BaseModel):
    id: int
    title: str
    target_role: str
    difficulty: str
    year_suitability: List[int]
    problem_statement: str
    relevance: str
    skills: List[str]
    duration_hours: int
    milestones: List[Dict[str, Any]]
    architecture: str
    datasets: List[str]
    deliverables: List[str]
    evaluation_checklist: List[str]
    extensions: List[str]

    class Config:
        from_attributes = True


class UserProjectCreateRequest(BaseModel):
    template_id: Optional[int] = None
    title: str = Field(..., min_length=3, max_length=200)
    github_url: Optional[str] = None
    notes: Optional[str] = None


class UserProjectUpdateRequest(BaseModel):
    status: Optional[str] = None  # planned, in progress, completed, submitted
    github_url: Optional[str] = None
    notes: Optional[str] = None
    progress_percent: Optional[int] = Field(None, ge=0, le=100)

    @field_validator("github_url")
    @classmethod
    def validate_github_url(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        pattern = r"^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9_\-\.]+\/[a-zA-Z0-9_\-\.]+\/?$"
        if not re.match(pattern, v):
            raise ValueError("Invalid GitHub repository URL format. Example: https://github.com/username/repository")
        return v


class UserProjectResponse(BaseModel):
    id: int
    template_id: Optional[int]
    title: str
    status: str
    github_url: Optional[str]
    notes: Optional[str]
    progress_percent: int
    created_at: datetime
    updated_at: datetime
    template: Optional[ProjectTemplateItem] = None

    class Config:
        from_attributes = True
