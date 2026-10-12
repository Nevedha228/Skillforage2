from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class ExternalResourceItem(BaseModel):
    title: str
    url: str
    type: str


class QuizQuestionItem(BaseModel):
    question: str
    options: List[str]
    # correct_answer omitted in public view!


class LessonListItem(BaseModel):
    id: int
    skill_category: str
    title: str
    difficulty: str
    estimated_minutes: int
    is_completed: bool = False
    is_bookmarked: bool = False

    class Config:
        from_attributes = True


class LessonDetailResponse(BaseModel):
    id: int
    skill_category: str
    title: str
    difficulty: str
    estimated_minutes: int
    content_markdown: str
    external_resources: List[ExternalResourceItem]
    quiz: QuizQuestionItem
    is_completed: bool = False
    is_bookmarked: bool = False
    quiz_passed: bool = False
    time_spent_minutes: int = 0


class QuizSubmitRequest(BaseModel):
    selected_answer: str
    time_spent_minutes: Optional[int] = 5


class QuizSubmitResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    lesson_completed: bool
    xp_awarded: int
    message: str


class BookmarkToggleRequest(BaseModel):
    is_bookmarked: bool
