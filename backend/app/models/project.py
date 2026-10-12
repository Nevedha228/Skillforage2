from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class ProjectTemplate(Base):
    __tablename__ = "project_templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    target_role = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    year_suitability = Column(JSON, nullable=False, default=list)  # [1, 2, 3, 4]
    problem_statement = Column(String(2000), nullable=False)
    relevance = Column(String(2000), nullable=False)
    skills = Column(JSON, nullable=False, default=list)
    duration_hours = Column(Integer, default=20, nullable=False)
    milestones = Column(JSON, nullable=False, default=list)
    architecture = Column(String(2000), nullable=False)
    datasets = Column(JSON, nullable=False, default=list)
    deliverables = Column(JSON, nullable=False, default=list)
    evaluation_checklist = Column(JSON, nullable=False, default=list)
    extensions = Column(JSON, nullable=False, default=list)


class UserProject(Base):
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id = Column(Integer, ForeignKey("project_templates.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    status = Column(String(50), default="planned", nullable=False)  # planned, in progress, completed, submitted
    github_url = Column(String(500), nullable=True)
    notes = Column(String(2000), nullable=True)
    progress_percent = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="projects")
    template = relationship("ProjectTemplate")
