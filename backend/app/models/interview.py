from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = Column(String(50), nullable=False)
    interview_type = Column(String(50), nullable=False)  # technical, behavioral, sql, programming, project, hr
    difficulty = Column(String(50), nullable=False)
    questions_and_answers = Column(JSON, nullable=False, default=list)
    rubric_scores = Column(JSON, nullable=False, default=dict)  # correctness, clarity, completeness, approach, structure, communication
    feedback = Column(JSON, nullable=False, default=dict)  # strengths, areas_for_improvement, recommendations
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="interviews")
