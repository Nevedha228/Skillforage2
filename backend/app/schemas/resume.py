from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ResumeStructuredData(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    education: List[Dict[str, Any]] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    experience: List[Dict[str, Any]] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)


class ATSAnalysisResponse(BaseModel):
    ats_score_estimate: int  # 0 to 100
    disclaimer: str
    section_presence: Dict[str, bool]
    found_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    job_match_score: Optional[int] = None
    missing_job_keywords: Optional[List[str]] = None


class ResumeProfileResponse(BaseModel):
    id: int
    structured_data: ResumeStructuredData
    ats_score_estimate: int
    ats_feedback: Dict[str, Any]
    keep_raw_file: bool
    updated_at: datetime


class CompareJobDescriptionRequest(BaseModel):
    job_description: str


class UpdateResumeRequest(BaseModel):
    structured_data: ResumeStructuredData
    keep_raw_file: Optional[bool] = False
