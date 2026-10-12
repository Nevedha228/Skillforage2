from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.database.database import get_db
from app.models import HackathonEvent
from app.schemas.hackathon import HackathonEventItem, HackathonPopupResponse

router = APIRouter(prefix="/hackathons", tags=["Hackathons Directory"])

HACKATHON_DISCLAIMER = (
    "Notice: Hackathon dates and details are demonstration entries curated for student discovery. "
    "Always verify submission deadlines and guidelines on the official organizer website."
)

@router.get("", response_model=List[HackathonEventItem])
def list_hackathons(
    mode: Optional[str] = None,  # online, offline, hybrid
    location: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(HackathonEvent)

    if mode:
        query = query.filter(HackathonEvent.mode == mode.lower())
    if location:
        query = query.filter(HackathonEvent.location.ilike(f"%{location}%"))
    if search:
        query = query.filter(
            (HackathonEvent.name.ilike(f"%{search}%")) |
            (HackathonEvent.description.ilike(f"%{search}%"))
        )

    return query.all()


@router.get("/popup", response_model=HackathonPopupResponse)
def get_landing_hackathon_popup(db: Session = Depends(get_db)):
    """
    Returns upcoming featured hackathon for the landing page popup.
    Dismissible and displayed once per session in frontend.
    """
    event = db.query(HackathonEvent).order_by(HackathonEvent.id.asc()).first()
    if not event:
        return HackathonPopupResponse(
            show_popup=False,
            event=None,
            data_last_updated=datetime.utcnow().strftime("%Y-%m-%d"),
            disclaimer=HACKATHON_DISCLAIMER
        )

    return HackathonPopupResponse(
        show_popup=True,
        event=HackathonEventItem.model_validate(event),
        data_last_updated=event.last_verified or datetime.utcnow().strftime("%Y-%m-%d"),
        disclaimer=HACKATHON_DISCLAIMER
    )


@router.post("/import")
async def import_hackathons(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        data = json.loads(content.decode("utf-8"))
        if not isinstance(data, list):
            data = [data]

        count = 0
        for item in data:
            db.add(HackathonEvent(
                name=item["name"],
                organizer=item["organizer"],
                mode=item.get("mode", "online"),
                location=item.get("location", "Virtual"),
                date=item["date"],
                deadline=item["deadline"],
                eligibility=item.get("eligibility", "College Students"),
                description=item["description"],
                official_link=item["official_link"],
                source=item.get("source", "Imported Feed"),
                last_verified=item.get("last_verified", datetime.utcnow().strftime("%Y-%m-%d")),
                is_demo=False
            ))
            count += 1
        db.commit()
        return {"success": True, "imported_count": count}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Import failed: {str(e)}")
