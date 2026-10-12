from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class SkillTaxonomy(Base):
    __tablename__ = "skill_taxonomy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    synonyms = Column(JSON, nullable=False, default=list)
    description = Column(String(500), nullable=True)


class UserSkillVerification(Base):
    __tablename__ = "user_skill_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="Not assessed")
    evidence_sources = Column(JSON, nullable=False, default=list)
    last_evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="skill_verifications")
