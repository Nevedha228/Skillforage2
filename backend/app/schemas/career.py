from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class CareerQuestionnaireRequest(BaseModel):
    interests: List[str] = Field(default_factory=list)
    activities: List[str] = Field(default_factory=list)
    problem_solving_style: Optional[str] = "analytical"  # analytical, creative, systematic, collaborative
    known_skills: List[str] = Field(default_factory=list)
    favorite_subjects: List[str] = Field(default_factory=list)
    career_goals: Optional[str] = "high_growth"  # high_growth, research, entrepreneurship, stable
    work_style: Optional[str] = "flexible"  # solo, team, flexible
    confidence_level: Optional[int] = 3  # 1 to 5
    learning_style: Optional[str] = "practical"  # practical, visual, theoretical


class RoleMatchExplanation(BaseModel):
    matching_interests: List[str]
    strengths: List[str]
    missing_skills: List[str]
    match_breakdown: Dict[str, float]  # interest_score, skill_score, activity_score
    summary: str


class CareerRoleMatch(BaseModel):
    id: str
    title: str
    category: str
    description: str
    match_score: int  # 0 to 100
    explanation: RoleMatchExplanation
    responsibilities: List[str]
    learning_priorities: List[str]
    related_roles: List[str]


class CareerDiscoveryResponse(BaseModel):
    disclaimer: str
    recommended_roles: List[CareerRoleMatch]
    total_evaluated: int


class SetTargetRoleRequest(BaseModel):
    role_id: str


class CompareRolesRequest(BaseModel):
    role_ids: List[str]
