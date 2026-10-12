from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class HackathonEvent(Base):
    __tablename__ = "hackathon_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    organizer = Column(String(200), nullable=False)
    mode = Column(String(50), default="online", nullable=False)  # online, offline, hybrid
    location = Column(String(100), default="Global / Virtual", nullable=False)
    date = Column(String(100), nullable=False)
    deadline = Column(String(100), nullable=False)
    eligibility = Column(String(200), default="College Students (Year 1-4)", nullable=False)
    description = Column(String(2000), nullable=False)
    official_link = Column(String(500), nullable=False)
    source = Column(String(100), default="Curated Student Hackathons", nullable=False)
    last_verified = Column(String(100), nullable=False)
    is_demo = Column(Boolean, default=True, nullable=False)
