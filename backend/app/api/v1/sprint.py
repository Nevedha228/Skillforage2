from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, CareerRole
from app.schemas.sprint import EmergencySprintRequest, EmergencySprintResponse, SprintDayPlan

router = APIRouter(prefix="/sprint", tags=["Emergency Placement Sprint"])

@router.post("/plan", response_model=EmergencySprintResponse)
def create_emergency_sprint_plan(
    req: EmergencySprintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    days = req.days_left
    hours = req.hours_per_day
    total_hours = round(days * hours, 1)

    role = db.query(CareerRole).filter(CareerRole.id == req.target_role).first()
    role_title = role.title if role else req.target_role

    schedule = []
    topics = [
        "Core DSA: Arrays, Strings, Hash Tables & Two Pointers",
        "Core DSA: Trees, Binary Search & Recursion",
        "SQL Querying: Joins, Aggregations, Window Functions",
        "System Architecture & API Fundamentals (REST, HTTP)",
        "Object-Oriented Design & Database Normalization",
        "Target Role Technical Deep-Dive & Architecture Patterns",
        "Resume Line-by-Line Technical Defense & Projects",
        "Behavioral Interview Preparation with STAR Methodology",
        "Timed High-Frequency Mock Technical Problems",
        "Full Loop Mock Interview Simulation & Gap Review"
    ]

    for d in range(1, days + 1):
        topic_idx = (d - 1) % len(topics)
        focus = topics[topic_idx]

        checklist = [
            f"Review top 5 standard patterns in {focus.split(':')[0]}",
            f"Solve 2 high-frequency interview problems under a 45-minute timer",
            "Write down 3 concise bullet points defending design tradeoffs"
        ]

        practice = [
            "Explain your logic out loud while writing solution code",
            "Check for edge cases: empty inputs, single element, boundary limits"
        ]

        milestone = None
        if d == days // 2:
            milestone = "Mid-Sprint Technical Checkpoint: Complete an Intermediate assessment"
        elif d == days:
            milestone = "Final Interview Readiness Checkpoint: Full simulated technical drill"

        schedule.append(SprintDayPlan(
            day_number=d,
            focus_topic=focus,
            time_allocation_hours=hours,
            checklist=checklist,
            practice_tasks=practice,
            milestone_check=milestone
        ))

    checkpoints = [
        {"day": 1, "action": "Baseline Assessment & Resume Review"},
        {"day": max(2, days // 2), "action": "Mid-Point Technical Assessment & Mock Interview"},
        {"day": days, "action": "Final Readiness Verification & Rest Before Drive"}
    ]

    msg = (
        f"Emergency Sprint configured for {role_title} with {days} days remaining at {hours:.1f} hours/day. "
        f"Stay disciplined with daily checklists, and adapt pacing if needed without penalty."
    )

    return EmergencySprintResponse(
        target_role=role_title,
        duration_days=days,
        total_dedicated_hours=total_hours,
        readiness_target_score=80 if days >= 14 else 70,
        daily_schedule=schedule,
        critical_checkpoints=checkpoints,
        guidance_message=msg
    )
