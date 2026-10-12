from sqlalchemy import Column, String, Boolean, JSON
from app.database.database import Base

class CareerRole(Base):
    __tablename__ = "career_roles"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    responsibilities = Column(JSON, nullable=False, default=list)
    required_skills = Column(JSON, nullable=False, default=dict)  # {skill: weight}
    interest_tags = Column(JSON, nullable=False, default=list)
    learning_priorities = Column(JSON, nullable=False, default=list)
    related_roles = Column(JSON, nullable=False, default=list)
    is_demo = Column(Boolean, default=False, nullable=False)
