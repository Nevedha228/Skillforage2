from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    year = Column(Integer, default=1, nullable=False)
    degree = Column(String(100), default="B.Tech.", nullable=False)
    branch = Column(String(100), default="Computer Science", nullable=False)
    target_role = Column(String(100), nullable=True)
    timezone = Column(String(100), default="UTC", nullable=False)
    daily_study_hours = Column(Float, default=1.5, nullable=False)
    learning_style = Column(String(100), default="practical", nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("UserAssessment", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("UserRoadmap", back_populates="user", cascade="all, delete-orphan")
    learning_progress = relationship("UserLearningProgress", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("UserProject", back_populates="user", cascade="all, delete-orphan")
    challenges = relationship("UserChallenge", back_populates="user", cascade="all, delete-orphan")
    xp_logs = relationship("UserXPLog", back_populates="user", cascade="all, delete-orphan")
    daily_activities = relationship("DailyActivity", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    resume = relationship("UserResume", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skill_verifications = relationship("UserSkillVerification", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="sessions")


class OTPCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    otp_hash = Column(String(64), nullable=False)
    purpose = Column(String(50), default="register", nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
