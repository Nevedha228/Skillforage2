from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import (
    User,
    UserAssessment,
    UserSkillVerification,
    UserRoadmap,
    UserProject,
    UserXPLog,
    DailyActivity,
    InterviewSession,
    CareerRole
)
from app.schemas.dashboard import DashboardStats
from app.services.rewards_service import calculate_user_rewards

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardStats)
def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    uid = current_user.id

    # 1. Assessments
    assessments = db.query(UserAssessment).filter(UserAssessment.user_id == uid).all()
    total_assessments = len(assessments)
    avg_score = round(sum(a.percentage for a in assessments) / total_assessments, 1) if total_assessments > 0 else 0.0

    # 2. Verified skills
    verified_skills_count = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == uid,
        UserSkillVerification.status.in_(["Demonstrated", "Strong evidence"])
    ).count()

    # 3. Roadmap progress
    roadmap = db.query(UserRoadmap).filter(UserRoadmap.user_id == uid).order_by(UserRoadmap.updated_at.desc()).first()
    roadmap_pct = 0.0
    if roadmap:
        all_task_ids = []
        for p in (roadmap.phases or []):
            for t in p.get("tasks", []):
                all_task_ids.append(t["id"])
        completed_ids = set(roadmap.completed_task_ids or [])
        completed_count = len(completed_ids.intersection(set(all_task_ids)))
        roadmap_pct = round((completed_count / max(len(all_task_ids), 1)) * 100, 1)

    # 4. Rewards & Streaks
    rewards = calculate_user_rewards(current_user, db)

    # 5. Projects
    projects_count = db.query(UserProject).filter(UserProject.user_id == uid).count()

    # 6. Mock interviews
    interviews_count = db.query(InterviewSession).filter(InterviewSession.user_id == uid).count()

    # Empty state evaluation
    is_empty = (total_assessments == 0 and roadmap is None and projects_count == 0)

    # Onboarding Checklist
    target_role_title = None
    if current_user.target_role:
        role_record = db.query(CareerRole).filter(CareerRole.id == current_user.target_role).first()
        target_role_title = role_record.title if role_record else current_user.target_role

    checklist = [
        {
            "id": "step_target_role",
            "title": "Select Target Career Role",
            "is_complete": bool(current_user.target_role),
            "action_url": "/careers"
        },
        {
            "id": "step_skill_assessment",
            "title": "Complete First Skill Assessment",
            "is_complete": (total_assessments > 0),
            "action_url": "/assessments"
        },
        {
            "id": "step_roadmap",
            "title": "Review Adaptive Learning Roadmap",
            "is_complete": (roadmap is not None),
            "action_url": "/roadmap"
        },
        {
            "id": "step_resume",
            "title": "Upload Resume & Check ATS Compatibility",
            "is_complete": (current_user.resume is not None),
            "action_url": "/resume"
        },
        {
            "id": "step_project",
            "title": "Start a Capstone Portfolio Project",
            "is_complete": (projects_count > 0),
            "action_url": "/projects"
        }
    ]

    # Next suggested action
    if not current_user.target_role:
        suggested = {
            "title": "Discover Your Career Path",
            "description": "Take the career discovery questionnaire to match with high-demand roles.",
            "button_text": "Explore Careers",
            "url": "/careers"
        }
    elif total_assessments == 0:
        suggested = {
            "title": "Benchmark Your Technical Skills",
            "description": f"Take a baseline assessment in {current_user.target_role.upper() if current_user.target_role else 'Python'} to uncover gaps.",
            "button_text": "Take Assessment",
            "url": "/assessments"
        }
    elif not roadmap or roadmap_pct == 0.0:
        suggested = {
            "title": "Start Your Adaptive Roadmap",
            "description": "Work on Phase 1 tasks tailored to your college year and market priorities.",
            "button_text": "Open Roadmap",
            "url": "/roadmap"
        }
    else:
        suggested = {
            "title": "Practice Mock Technical Interview",
            "description": "Drill high-frequency technical questions with instant rubric feedback.",
            "button_text": "Start Mock Interview",
            "url": "/interviews"
        }

    # Recent activities (from real logs)
    recent_activities = []
    for a in assessments[:3]:
        recent_activities.append({
            "type": "assessment",
            "title": f"Completed {a.category} Assessment ({a.difficulty})",
            "detail": f"Scored {a.percentage}% in {a.time_taken_seconds}s",
            "date": a.created_at.strftime("%Y-%m-%d")
        })

    return DashboardStats(
        is_empty_state=is_empty,
        username=current_user.username,
        year=current_user.year,
        degree=current_user.degree,
        branch=current_user.branch,
        target_role=current_user.target_role,
        target_role_title=target_role_title,
        total_assessments_taken=total_assessments,
        average_assessment_score=avg_score,
        total_verified_skills=verified_skills_count,
        roadmap_progress_percentage=roadmap_pct,
        total_xp=rewards.total_xp,
        current_streak_days=rewards.current_streak_days,
        total_projects_count=projects_count,
        interviews_practiced_count=interviews_count,
        onboarding_checklist=checklist,
        suggested_next_action=suggested,
        recent_activities=recent_activities
    )
