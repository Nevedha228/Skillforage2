from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SkillVerificationItem(BaseModel):
    id: int
    skill_name: str
    status: str  # "Not assessed", "Self-reported", "In progress", "Demonstrated", "Strong evidence"
    evidence_sources: List[Dict[str, Any]]
    last_evaluated_at: datetime

    class Config:
        from_attributes = True


class SelfReportSkillRequest(BaseModel):
    skill_name: str


class SkillTaxonomyItem(BaseModel):
    name: str
    category: str
    synonyms: List[str]
    description: str

    class Config:
        from_attributes = True
