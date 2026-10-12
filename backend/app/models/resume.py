from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserResume(Base):
    __tablename__ = "user_resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    raw_text = Column(String(20000), nullable=True)
    structured_data = Column(JSON, nullable=False, default=dict)  # summary, education, skills, projects, experience
    ats_score_estimate = Column(Integer, default=0, nullable=False)
    ats_feedback = Column(JSON, nullable=False, default=dict)  # missing_keywords, suggestions, etc.
    keep_raw_file = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="resume")
