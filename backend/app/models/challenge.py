from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    challenge_type = Column(String(50), default="daily", nullable=False)  # daily, weekly
    skill_category = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    hints = Column(JSON, nullable=False, default=list)
    xp_reward = Column(Integer, default=50, nullable=False)
    solution_type = Column(String(50), default="quiz", nullable=False)
    verification_rules = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, default=True, nullable=False)


class UserChallenge(Base):
    __tablename__ = "user_challenges"
    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", name="uq_user_challenge"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="challenges")
    challenge = relationship("Challenge")


class UserXPLog(Base):
    __tablename__ = "user_xp_logs"
    __table_args__ = (
        UniqueConstraint("user_id", "action_type", "reference_id", name="uq_user_xp_action"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(100), nullable=False)  # challenge, lesson, assessment, project
    reference_id = Column(String(100), nullable=False)
    xp_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="xp_logs")


class DailyActivity(Base):
    __tablename__ = "daily_activities"
    __table_args__ = (
        UniqueConstraint("user_id", "date_str", name="uq_user_daily_activity"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date_str = Column(String(20), nullable=False, index=True)  # YYYY-MM-DD
    actions_count = Column(Integer, default=1, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    last_active_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="daily_activities")
