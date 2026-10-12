from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, UserRoadmap, UserXPLog, DailyActivity
from app.schemas.roadmap import (
    RoadmapResponse,
    GenerateRoadmapRequest,
    CompleteTaskRequest,
    RescheduleRoadmapRequest,
    RoadmapPhase,
    RoadmapTask
)
from app.services.roadmap_service import generate_adaptive_roadmap, reschedule_roadmap

router = APIRouter(prefix="/roadmaps", tags=["Adaptive Roadmap"])

def _format_roadmap_response(roadmap: UserRoadmap) -> RoadmapResponse:
    completed_set = set(roadmap.completed_task_ids or [])
    all_tasks = []
    formatted_phases = []

    for p in (roadmap.phases or []):
        tasks = []
        for t in p.get("tasks", []):
            task_obj = RoadmapTask(
                id=t["id"],
                title=t["title"],
                task_type=t.get("task_type", "lesson"),
                skill=t.get("skill", "General"),
                estimated_hours=t.get("estimated_hours", 4.0),
                is_completed=(t["id"] in completed_set),
                completion_criteria=t.get("completion_criteria", "Complete task"),
                resource_link=t.get("resource_link")
            )
            tasks.append(task_obj)
            all_tasks.append(task_obj)

        formatted_phases.append(RoadmapPhase(
            phase_number=p.get("phase_number", 1),
            title=p.get("title", "Phase"),
            focus=p.get("focus", ""),
            prerequisite_skills=p.get("prerequisite_skills", []),
            tasks=tasks,
            milestone=p.get("milestone", ""),
            estimated_weeks=p.get("estimated_weeks", 2)
        ))

    total_tasks = len(all_tasks)
    completed_count = len(completed_set.intersection(set(t.id for t in all_tasks)))
    progress = round((completed_count / max(total_tasks, 1)) * 100, 1)

    suggestion = None
    if roadmap.missed_tasks_count > 0:
        suggestion = {
            "missed_tasks": roadmap.missed_tasks_count,
            "message": "You have some tasks behind schedule. Would you like to reschedule non-judgmentally to stay on track?",
            "action": "reschedule"
        }

    return RoadmapResponse(
        id=roadmap.id,
        target_role=roadmap.target_role,
        target_role_title=roadmap.target_role_title,
        version=roadmap.version,
        year_emphasis=roadmap.year_emphasis,
        weekly_hours=roadmap.weekly_hours,
        total_phases=len(formatted_phases),
        total_tasks=total_tasks,
        completed_tasks_count=completed_count,
        progress_percentage=progress,
        phases=formatted_phases,
        missed_tasks_count=roadmap.missed_tasks_count,
        rescheduling_suggestion=suggestion,
        created_at=roadmap.created_at,
        updated_at=roadmap.updated_at
    )


@router.get("/current", response_model=RoadmapResponse)
def get_current_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == current_user.id
    ).order_by(UserRoadmap.updated_at.desc()).first()

    if not roadmap:
        # Generate default roadmap if none exists
        roadmap = generate_adaptive_roadmap(current_user, db)

    return _format_roadmap_response(roadmap)


@router.post("/generate", response_model=RoadmapResponse)
def create_roadmap(
    req: GenerateRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = generate_adaptive_roadmap(
        user=current_user,
        db=db,
        target_role_override=req.target_role,
        weekly_hours_override=req.weekly_hours
    )
    return _format_roadmap_response(roadmap)


@router.post("/complete-task", response_model=RoadmapResponse)
def mark_task_complete(
    req: CompleteTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == current_user.id
    ).order_by(UserRoadmap.updated_at.desc()).first()

    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found.")

    completed_ids = list(roadmap.completed_task_ids or [])
    if req.task_id not in completed_ids:
        completed_ids.append(req.task_id)
        roadmap.completed_task_ids = completed_ids
        roadmap.updated_at = datetime.utcnow()

        # Award XP for roadmap milestone task
        ref_id = f"roadmap_{roadmap.id}_task_{req.task_id}"
        existing_xp = db.query(UserXPLog).filter(
            UserXPLog.user_id == current_user.id,
            UserXPLog.action_type == "roadmap_task",
            UserXPLog.reference_id == ref_id
        ).first()

        if not existing_xp:
            db.add(UserXPLog(
                user_id=current_user.id,
                action_type="roadmap_task",
                reference_id=ref_id,
                xp_amount=40,
                created_at=datetime.utcnow()
            ))

        # Record daily activity
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        daily = db.query(DailyActivity).filter(
            DailyActivity.user_id == current_user.id,
            DailyActivity.date_str == today_str
        ).first()

        if not daily:
            db.add(DailyActivity(
                user_id=current_user.id,
                date_str=today_str,
                actions_count=1,
                xp_earned=40,
                last_active_at=datetime.utcnow()
            ))
        else:
            daily.actions_count += 1
            daily.xp_earned += 40
            daily.last_active_at = datetime.utcnow()

        db.commit()
        db.refresh(roadmap)

    return _format_roadmap_response(roadmap)


@router.post("/reschedule", response_model=RoadmapResponse)
def trigger_reschedule(
    req: RescheduleRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == current_user.id
    ).order_by(UserRoadmap.updated_at.desc()).first()

    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found.")

    updated = reschedule_roadmap(
        roadmap=roadmap,
        reason=req.reason or "Pacing adjustment",
        adjusted_weekly_hours=req.adjusted_weekly_hours,
        db=db
    )
    return _format_roadmap_response(updated)
