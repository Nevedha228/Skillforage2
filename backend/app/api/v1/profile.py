from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import verify_password, hash_password
from app.core.deps import get_current_user
from app.models import (
    User,
    UserAssessment,
    UserRoadmap,
    UserLearningProgress,
    UserProject,
    UserChallenge,
    UserXPLog,
    InterviewSession,
    UserResume,
    UserSkillVerification
)
from app.schemas.auth import UserResponse
from app.schemas.profile import (
    ProfileUpdateRequest,
    PasswordChangeRequest,
    DeleteAccountRequest,
    DataExportResponse
)

router = APIRouter(prefix="/profile", tags=["User Profile & Settings"])

@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("", response_model=UserResponse)
def update_profile(
    req: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if req.username is not None:
        current_user.username = req.username
    if req.year is not None:
        current_user.year = req.year
    if req.degree is not None:
        current_user.degree = req.degree
    if req.branch is not None:
        current_user.branch = req.branch
    if req.target_role is not None:
        current_user.target_role = req.target_role
    if req.timezone is not None:
        current_user.timezone = req.timezone
    if req.daily_study_hours is not None:
        current_user.daily_study_hours = req.daily_study_hours
    if req.learning_style is not None:
        current_user.learning_style = req.learning_style
    if req.notifications_enabled is not None:
        current_user.notifications_enabled = req.notifications_enabled

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password")
def change_password(
    req: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(req.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password entered is incorrect."
        )

    current_user.password_hash = hash_password(req.new_password)
    db.commit()
    return {"success": True, "message": "Password changed successfully."}


@router.get("/export-data")
def export_all_user_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exports all personal user records in standard JSON format.
    Enforces strict user ownership: only current_user's rows are retrieved.
    """
    uid = current_user.id

    assessments = db.query(UserAssessment).filter(UserAssessment.user_id == uid).all()
    roadmaps = db.query(UserRoadmap).filter(UserRoadmap.user_id == uid).all()
    progress = db.query(UserLearningProgress).filter(UserLearningProgress.user_id == uid).all()
    projects = db.query(UserProject).filter(UserProject.user_id == uid).all()
    challenges = db.query(UserChallenge).filter(UserChallenge.user_id == uid).all()
    xp_logs = db.query(UserXPLog).filter(UserXPLog.user_id == uid).all()
    interviews = db.query(InterviewSession).filter(InterviewSession.user_id == uid).all()
    resume = db.query(UserResume).filter(UserResume.user_id == uid).first()
    verifications = db.query(UserSkillVerification).filter(UserSkillVerification.user_id == uid).all()

    return {
        "user_profile": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "year": current_user.year,
            "degree": current_user.degree,
            "branch": current_user.branch,
            "target_role": current_user.target_role,
            "timezone": current_user.timezone,
            "daily_study_hours": current_user.daily_study_hours,
            "learning_style": current_user.learning_style,
            "created_at": current_user.created_at.isoformat()
        },
        "assessments": [
            {
                "id": a.id,
                "category": a.category,
                "difficulty": a.difficulty,
                "score": a.score,
                "max_score": a.max_score,
                "percentage": a.percentage,
                "time_taken_seconds": a.time_taken_seconds,
                "topic_breakdown": a.topic_breakdown,
                "weak_topics": a.weak_topics,
                "created_at": a.created_at.isoformat()
            }
            for a in assessments
        ],
        "roadmaps": [
            {
                "id": r.id,
                "target_role": r.target_role,
                "target_role_title": r.target_role_title,
                "version": r.version,
                "year_emphasis": r.year_emphasis,
                "phases": r.phases,
                "completed_task_ids": r.completed_task_ids,
                "created_at": r.created_at.isoformat()
            }
            for r in roadmaps
        ],
        "learning_progress": [
            {
                "lesson_id": p.lesson_id,
                "is_completed": p.is_completed,
                "time_spent_minutes": p.time_spent_minutes,
                "quiz_passed": p.quiz_passed,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None
            }
            for p in progress
        ],
        "projects": [
            {
                "id": pr.id,
                "title": pr.title,
                "status": pr.status,
                "github_url": pr.github_url,
                "progress_percent": pr.progress_percent
            }
            for pr in projects
        ],
        "challenges": [
            {"challenge_id": c.challenge_id, "completed_at": c.completed_at.isoformat()}
            for c in challenges
        ],
        "xp_history": [
            {"action_type": x.action_type, "xp_amount": x.xp_amount, "created_at": x.created_at.isoformat()}
            for x in xp_logs
        ],
        "interviews": [
            {
                "id": i.id,
                "target_role": i.target_role,
                "interview_type": i.interview_type,
                "difficulty": i.difficulty,
                "rubric_scores": i.rubric_scores,
                "created_at": i.created_at.isoformat()
            }
            for i in interviews
        ],
        "resume": {
            "structured_data": resume.structured_data,
            "ats_score_estimate": resume.ats_score_estimate,
            "updated_at": resume.updated_at.isoformat()
        } if resume else None,
        "skill_verifications": [
            {
                "skill_name": v.skill_name,
                "status": v.status,
                "evidence_sources": v.evidence_sources,
                "last_evaluated_at": v.last_evaluated_at.isoformat()
            }
            for v in verifications
        ]
    }


@router.delete("/delete-account")
def delete_account(
    req: DeleteAccountRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permanently deletes user account and cascading entities.
    Requires password confirmation.
    """
    if not verify_password(req.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password incorrect. Cannot delete account."
        )

    # Delete user record (cascades all sessions, assessments, roadmaps, etc.)
    db.delete(current_user)
    db.commit()

    # Clear cookie
    response.delete_cookie(key="sf_session", path="/")

    return {
        "success": True,
        "message": "Your account and all associated records have been permanently deleted."
    }
