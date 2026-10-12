from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, CareerRole
from app.schemas.career import (
    CareerQuestionnaireRequest,
    CareerDiscoveryResponse,
    SetTargetRoleRequest,
    CompareRolesRequest,
    CareerRoleMatch
)
from app.services.career_service import calculate_career_matches, HEURISTIC_DISCLAIMER

router = APIRouter(prefix="/careers", tags=["Career Discovery"])

@router.get("")
def list_career_roles(db: Session = Depends(get_db)):
    roles = db.query(CareerRole).all()
    return {
        "total": len(roles),
        "disclaimer": HEURISTIC_DISCLAIMER,
        "roles": [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category,
                "description": r.description,
                "responsibilities": r.responsibilities,
                "required_skills": r.required_skills,
                "interest_tags": r.interest_tags,
                "learning_priorities": r.learning_priorities,
                "related_roles": r.related_roles
            }
            for r in roles
        ]
    }


@router.get("/{role_id}")
def get_career_role(role_id: str, db: Session = Depends(get_db)):
    role = db.query(CareerRole).filter(CareerRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Career role '{role_id}' not found.")
    return {
        "id": role.id,
        "title": role.title,
        "category": role.category,
        "description": role.description,
        "responsibilities": role.responsibilities,
        "required_skills": role.required_skills,
        "interest_tags": role.interest_tags,
        "learning_priorities": role.learning_priorities,
        "related_roles": role.related_roles,
        "disclaimer": HEURISTIC_DISCLAIMER
    }


@router.post("/match", response_model=CareerDiscoveryResponse)
def match_careers(req: CareerQuestionnaireRequest, db: Session = Depends(get_db)):
    return calculate_career_matches(req, db)


@router.post("/compare")
def compare_roles(req: CompareRolesRequest, db: Session = Depends(get_db)):
    if len(req.role_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide at least 2 role IDs to compare."
        )

    roles = db.query(CareerRole).filter(CareerRole.id.in_(req.role_ids)).all()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="None of the specified roles were found.")

    return {
        "disclaimer": HEURISTIC_DISCLAIMER,
        "compared_roles": [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category,
                "description": r.description,
                "required_skills": r.required_skills,
                "responsibilities": r.responsibilities,
                "learning_priorities": r.learning_priorities,
                "related_roles": r.related_roles
            }
            for r in roles
        ]
    }


@router.post("/set-target")
def set_target_role(
    req: SetTargetRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = db.query(CareerRole).filter(CareerRole.id == req.role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Career role '{req.role_id}' not found.")

    current_user.target_role = role.id
    db.commit()

    return {
        "success": True,
        "message": f"Target role set to '{role.title}'. Your learning roadmap will adapt to this goal.",
        "target_role": role.id,
        "target_role_title": role.title
    }
