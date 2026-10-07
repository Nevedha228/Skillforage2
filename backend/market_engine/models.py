from dataclasses import dataclass
from typing import Optional


@dataclass
class JobPosting:
    source: str
    source_job_id: str

    title: str
    company: str
    location: str

    description: str
    url: str

    category: str = ""

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None

    contract_type: str = ""
    contract_time: str = ""

    created_at: str = ""

    collected_at: str = ""

    # Research metadata
    query: str = ""
    page: int = 1