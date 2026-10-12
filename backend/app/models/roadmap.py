from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserRoadmap(Base):
    __tablename__ = "user_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = Column(String(50), nullable=False)
    target_role_title = Column(String(100), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    year_emphasis = Column(String(100), nullable=False)
    weekly_hours = Column(Float, default=10.0, nullable=False)
    phases = Column(JSON, nullable=False, default=list)
    completed_task_ids = Column(JSON, nullable=False, default=list)
    missed_tasks_count = Column(Integer, default=0, nullable=False)
    rescheduling_history = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="roadmaps")
