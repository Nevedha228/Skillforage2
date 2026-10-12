from typing import List, Optional
from pydantic import BaseModel

class HackathonEventItem(BaseModel):
    id: int
    name: str
    organizer: str
    mode: str  # online, offline, hybrid
    location: str
    date: str
    deadline: str
    eligibility: str
    description: str
    official_link: str
    source: str
    last_verified: str
    is_demo: bool = True

    class Config:
        from_attributes = True


class HackathonPopupResponse(BaseModel):
    show_popup: bool
    event: Optional[HackathonEventItem] = None
    data_last_updated: str
    disclaimer: str
