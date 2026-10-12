from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, UserAssessment
from app.schemas.assessment import (
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    AssessmentHistoryResponse,
    AssessmentHistoryItem
)
from app.services.assessment_service import start_assessment, evaluate_assessment_submission

router = APIRouter(prefix="/assessments", tags=["Skill Assessments"])

@router.get("/categories")
def get_categories():
    return {
        "categories": [
            "Python",
            "SQL",
            "DSA",
            "DBMS",
            "OOP",
            "Web",
            "Statistics/Data Analysis",
            "Problem Solving"
        ],
        "difficulties": ["Beginner", "Intermediate", "Advanced"]
    }


@router.get("/start", response_model=AssessmentStartResponse)
def start_assessment_session(
    category: str = Query("Python"),
    difficulty: str = Query("Beginner"),
    db: Session = Depends(get_db)
):
    return start_assessment(category, difficulty, db)


@router.post("/submit", response_model=AssessmentResultResponse)
def submit_assessment(
    req: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return evaluate_assessment_submission(req, current_user.id, db)


@router.get("/history", response_model=AssessmentHistoryResponse)
def get_assessment_history(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    sort_by: str = Query("date_desc"),  # date_desc, date_asc, score_desc, score_asc
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(UserAssessment).filter(UserAssessment.user_id == current_user.id)

    if category:
        query = query.filter(UserAssessment.category == category)
    if difficulty:
        query = query.filter(UserAssessment.difficulty == difficulty)

    if sort_by == "date_asc":
        query = query.order_by(UserAssessment.created_at.asc())
    elif sort_by == "score_desc":
        query = query.order_by(UserAssessment.percentage.desc())
    elif sort_by == "score_asc":
        query = query.order_by(UserAssessment.percentage.asc())
    else:
        query = query.order_by(UserAssessment.created_at.desc())

    records = query.all()

    total = len(records)
    avg_score = round(sum(r.percentage for r in records) / total, 1) if total > 0 else 0.0
    best_score = max((r.percentage for r in records), default=0.0)

    items = [
        AssessmentHistoryItem(
            id=r.id,
            category=r.category,
            difficulty=r.difficulty,
            score=r.score,
            max_score=r.max_score,
            percentage=r.percentage,
            time_taken_seconds=r.time_taken_seconds,
            weak_topics=r.weak_topics or [],
            created_at=r.created_at
        )
        for r in records
    ]

    return AssessmentHistoryResponse(
        total_taken=total,
        average_percentage=avg_score,
        best_percentage=best_score,
        assessments=items
    )


@router.get("/history/{assessment_id}")
def get_assessment_detail(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(UserAssessment).filter(
        UserAssessment.id == assessment_id,
        UserAssessment.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment record not found or does not belong to you."
        )

    return {
        "id": record.id,
        "category": record.category,
        "difficulty": record.difficulty,
        "score": record.score,
        "max_score": record.max_score,
        "percentage": record.percentage,
        "time_taken_seconds": record.time_taken_seconds,
        "topic_breakdown": record.topic_breakdown,
        "weak_topics": record.weak_topics,
        "recommendations": record.recommendations,
        "created_at": record.created_at.isoformat()
    }
