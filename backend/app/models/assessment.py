from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    difficulty = Column(String(50), nullable=False, index=True)
    question_type = Column(String(50), default="multiple_choice", nullable=False)
    question_text = Column(String(2000), nullable=False)
    options = Column(JSON, nullable=False, default=list)
    correct_answer = Column(String(500), nullable=False)
    topic_tag = Column(String(100), nullable=False)
    explanation = Column(String(2000), nullable=False)
    code_starter = Column(String(2000), nullable=True)
    test_cases_or_rubric = Column(JSON, nullable=True)


class UserAssessment(Base):
    __tablename__ = "user_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    topic_breakdown = Column(JSON, nullable=False, default=dict)
    weak_topics = Column(JSON, nullable=False, default=list)
    recommendations = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="assessments")
