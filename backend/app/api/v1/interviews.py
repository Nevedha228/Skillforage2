from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, InterviewSession
from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewSubmitRequest,
    InterviewSubmitResponse,
    InterviewHistoryItem
)
from app.services.interview_service import (
    start_interview_session,
    evaluate_interview_rubric,
    INTERVIEW_DISCLAIMER
)

router = APIRouter(prefix="/interviews", tags=["Interview Hub"])

@router.post("/start", response_model=InterviewStartResponse)
def start_interview(
    req: InterviewStartRequest,
    current_user: User = Depends(get_current_user)
):
    return start_interview_session(
        target_role=req.target_role,
        interview_type=req.interview_type,
        difficulty=req.difficulty
    )


@router.post("/submit", response_model=InterviewSubmitResponse)
def submit_interview(
    req: InterviewSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return evaluate_interview_rubric(req, current_user.id, db)


@router.get("/history", response_model=List[InterviewHistoryItem])
def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

    return [
        InterviewHistoryItem(
            id=s.id,
            target_role=s.target_role,
            interview_type=s.interview_type,
            difficulty=s.difficulty,
            total_percentage=s.rubric_scores.get("total_percentage", 0.0) if s.rubric_scores else 0.0,
            created_at=s.created_at
        )
        for s in sessions
    ]


@router.get("/history/{session_id}")
def get_interview_session_detail(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_record = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or does not belong to you."
        )

    return {
        "id": session_record.id,
        "target_role": session_record.target_role,
        "interview_type": session_record.interview_type,
        "difficulty": session_record.difficulty,
        "questions_and_answers": session_record.questions_and_answers,
        "rubric_scores": session_record.rubric_scores,
        "feedback": session_record.feedback,
        "time_taken_seconds": session_record.time_taken_seconds,
        "disclaimer": INTERVIEW_DISCLAIMER,
        "created_at": session_record.created_at.isoformat()
    }
