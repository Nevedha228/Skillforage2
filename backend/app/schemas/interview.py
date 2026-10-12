from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class InterviewQuestion(BaseModel):
    id: int
    question: str
    category: str
    key_aspects: List[str]


class InterviewStartRequest(BaseModel):
    target_role: str
    interview_type: str = "technical"  # technical, behavioral, sql, programming, project, hr
    difficulty: str = "Intermediate"


class InterviewStartResponse(BaseModel):
    session_id: str
    target_role: str
    interview_type: str
    difficulty: str
    questions: List[InterviewQuestion]
    time_limit_minutes: int
    disclaimer: str


class AnswerItem(BaseModel):
    question_id: int
    question: str
    answer_text: str


class InterviewSubmitRequest(BaseModel):
    target_role: str
    interview_type: str
    difficulty: str
    time_taken_seconds: int
    answers: List[AnswerItem]


class RubricBreakdown(BaseModel):
    correctness: float  # 0 to 100
    clarity: float
    completeness: float
    approach: float
    structure: float
    communication: float
    total_percentage: float


class InterviewFeedback(BaseModel):
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]
    llm_status: str  # "heuristic_rubric_fallback" or "ai_evaluated"


class InterviewSubmitResponse(BaseModel):
    id: int
    target_role: str
    interview_type: str
    difficulty: str
    time_taken_seconds: int
    rubric_scores: RubricBreakdown
    feedback: InterviewFeedback
    disclaimer: str
    created_at: datetime


class InterviewHistoryItem(BaseModel):
    id: int
    target_role: str
    interview_type: str
    difficulty: str
    total_percentage: float
    created_at: datetime

    class Config:
        from_attributes = True
