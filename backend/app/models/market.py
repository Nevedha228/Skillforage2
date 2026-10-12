from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from app.database.database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)
    source_job_id = Column(String(100), nullable=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False)
    location = Column(String(100), nullable=False, index=True)
    description = Column(String(10000), nullable=False)
    url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=False, index=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    experience_level = Column(String(50), default="entry", nullable=False)  # entry, mid, senior
    skills_extracted = Column(JSON, nullable=False, default=list)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)
    data_origin = Column(String(50), default="synthetic_demo", nullable=False, index=True)  # collected, imported, synthetic_demo
    posted_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MarketRun(Base):
    __tablename__ = "market_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False)
    query_role = Column(String(100), nullable=False)
    country = Column(String(10), default="in", nullable=False)
    location = Column(String(100), nullable=True)
    jobs_collected = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="completed", nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("market_runs.id"), nullable=True)
    role = Column(String(100), nullable=False, index=True)
    total_jobs = Column(Integer, default=0, nullable=False)
    top_skills = Column(JSON, nullable=False, default=list)
    is_demo = Column(Boolean, default=False, nullable=False)
    data_origin = Column(String(50), default="synthetic_demo", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
