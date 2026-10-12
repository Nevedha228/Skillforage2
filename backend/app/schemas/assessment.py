from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class QuestionPublic(BaseModel):
    id: int
    category: str
    difficulty: str
    question_type: str
    question_text: str
    options: List[str]
    topic_tag: str
    code_starter: Optional[str] = None

    class Config:
        from_attributes = True


class AssessmentStartResponse(BaseModel):
    category: str
    difficulty: str
    total_questions: int
    time_limit_seconds: int
    questions: List[QuestionPublic]


class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: str


class AssessmentSubmitRequest(BaseModel):
    category: str
    difficulty: str
    time_taken_seconds: int = Field(..., ge=0)
    answers: List[AnswerSubmission]


class TopicScore(BaseModel):
    correct: int
    total: int
    percentage: float


class QuestionReviewItem(BaseModel):
    question_id: int
    question_text: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    topic_tag: str


class AssessmentResultResponse(BaseModel):
    id: int
    category: str
    difficulty: str
    score: float
    max_score: float
    percentage: float
    proficiency_level: str  # Foundational, Developing, Competent, Advanced
    time_taken_seconds: int
    topic_breakdown: Dict[str, TopicScore]
    weak_topics: List[str]
    recommendations: List[str]
    verification_status: str  # In progress, Demonstrated, Strong evidence
    review: List[QuestionReviewItem]


class AssessmentHistoryItem(BaseModel):
    id: int
    category: str
    difficulty: str
    score: float
    max_score: float
    percentage: float
    time_taken_seconds: int
    weak_topics: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentHistoryResponse(BaseModel):
    total_taken: int
    average_percentage: float
    best_percentage: float
    assessments: List[AssessmentHistoryItem]
