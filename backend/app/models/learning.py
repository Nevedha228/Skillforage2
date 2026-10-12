from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    skill_category = Column(String(100), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    difficulty = Column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    content_markdown = Column(String(10000), nullable=False)
    estimated_minutes = Column(Integer, default=15, nullable=False)
    external_resources = Column(JSON, nullable=False, default=list)
    quiz = Column(JSON, nullable=False, default=dict)
    is_demo = Column(Boolean, default=False, nullable=False)


class UserLearningProgress(Base):
    __tablename__ = "user_learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    is_bookmarked = Column(Boolean, default=False, nullable=False)
    time_spent_minutes = Column(Integer, default=0, nullable=False)
    quiz_passed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="learning_progress")
    lesson = relationship("Lesson")
