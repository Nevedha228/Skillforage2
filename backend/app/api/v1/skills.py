from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, SkillTaxonomy, UserSkillVerification
from app.schemas.skill import SkillVerificationItem, SelfReportSkillRequest, SkillTaxonomyItem

router = APIRouter(prefix="/skills", tags=["Skills & Verification"])

@router.get("/taxonomy", response_model=List[SkillTaxonomyItem])
def get_skills_taxonomy(db: Session = Depends(get_db)):
    skills = db.query(SkillTaxonomy).all()
    return skills


@router.get("/verified", response_model=List[SkillVerificationItem])
def get_verified_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns user evidenced skill statuses.
    Allowed statuses: Not assessed, Self-reported, In progress, Demonstrated, Strong evidence.
    Never uses the term 'certified'.
    """
    records = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == current_user.id
    ).all()
    return records


@router.post("/self-report", response_model=SkillVerificationItem)
def self_report_skill(
    req: SelfReportSkillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill_name = req.skill_name.strip()
    if not skill_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill name cannot be empty.")

    record = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == current_user.id,
        UserSkillVerification.skill_name == skill_name
    ).first()

    now = datetime.utcnow()
    evidence_entry = {
        "type": "self_reported",
        "description": "Added directly by student in Skill Verification profile.",
        "date": now.isoformat()
    }

    if not record:
        record = UserSkillVerification(
            user_id=current_user.id,
            skill_name=skill_name,
            status="Self-reported",
            evidence_sources=[evidence_entry],
            last_evaluated_at=now
        )
        db.add(record)
    else:
        # If already Demonstrated or Strong evidence, don't downgrade
        if record.status in ["Not assessed", "In progress"]:
            record.status = "Self-reported"
        existing = record.evidence_sources or []
        existing.append(evidence_entry)
        record.evidence_sources = existing
        record.last_evaluated_at = now

    db.commit()
    db.refresh(record)
    return record
