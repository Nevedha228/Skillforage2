from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import (
    User,
    UserRoadmap,
    CareerRole,
    UserAssessment,
    UserSkillVerification
)
from app.services.market_service import compare_user_skill_gap
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapPhase,
    RoadmapTask
)

YEAR_EMPHASIS_MAP = {
    1: "Foundations & Exploration (Year 1: Programming basics, problem solving, computer science fundamentals)",
    2: "Core Engineering & DSA (Year 2: Data structures, algorithms, relational databases, OOP principles)",
    3: "Specialization & Portfolio (Year 3: Production frameworks, full-stack systems, internship prep)",
    4: "Placement Sprint & Interview Mastery (Year 4: High-frequency coding, system design, mock interviews, ATS resume)"
}

def generate_adaptive_roadmap(
    user: User,
    db: Session,
    target_role_override: Optional[str] = None,
    weekly_hours_override: Optional[float] = None
) -> UserRoadmap:
    target_role_id = target_role_override or user.target_role or "sde"
    weekly_hours = weekly_hours_override or user.daily_study_hours * 7 or 10.0

    role = db.query(CareerRole).filter(CareerRole.id == target_role_id).first()
    if not role:
        role = db.query(CareerRole).first()

    # Get skill gap analysis
    gap_data = compare_user_skill_gap(user.id, role.id, db)
    critical_gaps = [g["skill"] for g in gap_data["prioritized_gaps"] if g["priority"] == "Critical"]
    high_gaps = [g["skill"] for g in gap_data["prioritized_gaps"] if g["priority"] == "High"]
    other_gaps = [g["skill"] for g in gap_data["prioritized_gaps"] if g["priority"] == "Medium"]

    # Get recent assessment weak topics
    recent_assessments = db.query(UserAssessment).filter(UserAssessment.user_id == user.id).all()
    recent_weak_topics = []
    for a in recent_assessments:
        if a.weak_topics:
            recent_weak_topics.extend(a.weak_topics)

    student_year = user.year or 1
    year_emphasis = YEAR_EMPHASIS_MAP.get(student_year, YEAR_EMPHASIS_MAP[1])

    # Construct adaptive phases
    phases_data = []

    # Phase 1: Core Foundation & High-Priority Prerequisites
    p1_skills = critical_gaps[:2] or ["Programming Fundamentals", "Problem Solving"]
    p1_tasks = [
        {
            "id": "p1_t1",
            "title": f"Master Core Syntax and Architecture of {p1_skills[0]}",
            "task_type": "lesson",
            "skill": p1_skills[0],
            "estimated_hours": 6.0,
            "completion_criteria": "Complete interactive lessons and pass end-of-unit quiz with >= 80%."
        },
        {
            "id": "p1_t2",
            "title": f"Practical Problem Solving Drills in {p1_skills[0]}",
            "task_type": "exercise",
            "skill": p1_skills[0],
            "estimated_hours": 8.0,
            "completion_criteria": "Solve 10 foundational coding exercises on edge cases and data structures."
        }
    ]
    if len(p1_skills) > 1:
        p1_tasks.append({
            "id": "p1_t3",
            "title": f"Foundational Competency in {p1_skills[1]}",
            "task_type": "lesson",
            "skill": p1_skills[1],
            "estimated_hours": 6.0,
            "completion_criteria": "Complete guided tutorials and execute standard verification queries."
        })
    p1_tasks.append({
        "id": "p1_t4",
        "title": "Phase 1 Knowledge Checkpoint",
        "task_type": "checkpoint",
        "skill": "Assessment",
        "estimated_hours": 2.0,
        "completion_criteria": "Complete a timed Skill Assessment and achieve Competent status."
    })
    p1_total_hours = sum(t["estimated_hours"] for t in p1_tasks)
    p1_weeks = max(1, int(round(p1_total_hours / weekly_hours)))

    phases_data.append({
        "phase_number": 1,
        "title": "Phase 1: Essential Foundations & Prerequisite Gaps",
        "focus": f"Bridge critical market requirements in {', '.join(p1_skills)}.",
        "prerequisite_skills": [],
        "tasks": p1_tasks,
        "milestone": "Demonstrated foundational competence on core technical requirements.",
        "estimated_weeks": p1_weeks
    })

    # Phase 2: Core Engineering, Data Structures & Relational Systems
    p2_skills = high_gaps[:2] or ["Data Structures", "Relational Databases"]
    p2_tasks = [
        {
            "id": "p2_t1",
            "title": f"Deep Dive: Advanced Patterns in {p2_skills[0]}",
            "task_type": "lesson",
            "skill": p2_skills[0],
            "estimated_hours": 8.0,
            "completion_criteria": "Study algorithmic complexity, memory representation, and design tradeoffs."
        },
        {
            "id": "p2_t2",
            "title": "Build a Data Persistence Layer with Normalized Schema",
            "task_type": "exercise",
            "skill": "DBMS",
            "estimated_hours": 10.0,
            "completion_criteria": "Implement relational models with 3NF normalization, foreign keys, and indexes."
        },
        {
            "id": "p2_t3",
            "title": "Phase 2 Comprehensive Checkpoint",
            "task_type": "checkpoint",
            "skill": "Assessment",
            "estimated_hours": 2.0,
            "completion_criteria": "Score >= 75% on Intermediate technical assessment."
        }
    ]
    p2_total_hours = sum(t["estimated_hours"] for t in p2_tasks)
    p2_weeks = max(1, int(round(p2_total_hours / weekly_hours)))

    phases_data.append({
        "phase_number": 2,
        "title": "Phase 2: Core Engineering & Systems Implementation",
        "focus": f"Strengthen intermediate implementation skills in {', '.join(p2_skills)}.",
        "prerequisite_skills": p1_skills,
        "tasks": p2_tasks,
        "milestone": "Working database and backend components with automated unit tests.",
        "estimated_weeks": p2_weeks
    })

    # Phase 3: Applied Portfolio Project
    p3_tasks = [
        {
            "id": "p3_t1",
            "title": f"Design Architecture for {role.title} Portfolio Project",
            "task_type": "project",
            "skill": "System Design",
            "estimated_hours": 6.0,
            "completion_criteria": "Draft component diagram, API contract specs, and database schema."
        },
        {
            "id": "p3_t2",
            "title": "Implement Project Core Features and Integration",
            "task_type": "project",
            "skill": role.title,
            "estimated_hours": 16.0,
            "completion_criteria": "Complete core user workflows and connect persistent data storage."
        },
        {
            "id": "p3_t3",
            "title": "Publish Project to GitHub with Thorough README",
            "task_type": "project",
            "skill": "Git",
            "estimated_hours": 4.0,
            "completion_criteria": "Repository includes setup instructions, architecture rationale, and clean commits."
        }
    ]
    p3_total_hours = sum(t["estimated_hours"] for t in p3_tasks)
    p3_weeks = max(1, int(round(p3_total_hours / weekly_hours)))

    phases_data.append({
        "phase_number": 3,
        "title": "Phase 3: Portfolio Capstone Project",
        "focus": f"Build tangible proof of competence matching employer standards for {role.title}.",
        "prerequisite_skills": p1_skills + p2_skills,
        "tasks": p3_tasks,
        "milestone": "Completed and deployable portfolio project featured on GitHub.",
        "estimated_weeks": p3_weeks
    })

    # Phase 4: Interview Readiness & Placement Sprint
    p4_tasks = [
        {
            "id": "p4_t1",
            "title": f"Technical Mock Interview: {role.title} High-Frequency Questions",
            "task_type": "exercise",
            "skill": "Technical Interview",
            "estimated_hours": 6.0,
            "completion_criteria": "Complete mock interview session with rubric evaluation >= 70%."
        },
        {
            "id": "p4_t2",
            "title": "Resume Keyword Optimization and ATS Check",
            "task_type": "exercise",
            "skill": "Resume Engineering",
            "estimated_hours": 4.0,
            "completion_criteria": "Upload and align resume keywords against target role job description."
        },
        {
            "id": "p4_t3",
            "title": "Final Interview Readiness Benchmark",
            "task_type": "checkpoint",
            "skill": "Readiness",
            "estimated_hours": 3.0,
            "completion_criteria": "Complete behavioral and technical interview simulation."
        }
    ]
    p4_total_hours = sum(t["estimated_hours"] for t in p4_tasks)
    p4_weeks = max(1, int(round(p4_total_hours / weekly_hours)))

    phases_data.append({
        "phase_number": 4,
        "title": "Phase 4: Interview Readiness & Placement Sprints",
        "focus": "Transition from skill learning to high-pressure interview performance.",
        "prerequisite_skills": ["Portfolio Project", "Core CS"],
        "tasks": p4_tasks,
        "milestone": "Verified interview readiness score >= 75% and ATS-optimized resume.",
        "estimated_weeks": p4_weeks
    })

    # Check for existing roadmap to increment version
    existing_roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user.id,
        UserRoadmap.target_role == role.id
    ).first()

    version = 1
    history = []
    if existing_roadmap:
        version = existing_roadmap.version + 1
        history = existing_roadmap.rescheduling_history or []
        history.append({
            "version": version,
            "timestamp": datetime.utcnow().isoformat(),
            "reason": "Roadmap regenerated with updated skill gap assessment and pacing."
        })
        existing_roadmap.version = version
        existing_roadmap.year_emphasis = year_emphasis
        existing_roadmap.weekly_hours = weekly_hours
        existing_roadmap.phases = phases_data
        existing_roadmap.rescheduling_history = history
        existing_roadmap.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_roadmap)
        return existing_roadmap

    new_roadmap = UserRoadmap(
        user_id=user.id,
        target_role=role.id,
        target_role_title=role.title,
        version=1,
        year_emphasis=year_emphasis,
        weekly_hours=weekly_hours,
        phases=phases_data,
        completed_task_ids=[],
        missed_tasks_count=0,
        rescheduling_history=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)
    return new_roadmap


def reschedule_roadmap(
    roadmap: UserRoadmap,
    reason: str,
    adjusted_weekly_hours: Optional[float],
    db: Session
) -> UserRoadmap:
    """
    Non-judgmental rescheduling: re-spreads remaining incomplete tasks across
    adjusted weekly hours and provides an encouraging plain-language explanation.
    """
    completed_ids = set(roadmap.completed_task_ids or [])
    new_weekly_hours = adjusted_weekly_hours or roadmap.weekly_hours or 10.0

    # Calculate remaining tasks
    remaining_hours = 0.0
    for phase in (roadmap.phases or []):
        for task in phase.get("tasks", []):
            if task["id"] not in completed_ids:
                remaining_hours += task.get("estimated_hours", 4.0)

    # Recalculate phases weeks
    updated_phases = []
    for phase in (roadmap.phases or []):
        phase_copy = dict(phase)
        phase_incomplete_hours = sum(
            t.get("estimated_hours", 4.0)
            for t in phase.get("tasks", [])
            if t["id"] not in completed_ids
        )
        phase_copy["estimated_weeks"] = max(1, int(round(phase_incomplete_hours / new_weekly_hours))) if phase_incomplete_hours > 0 else 0
        updated_phases.append(phase_copy)

    explanation = (
        f"Your roadmap has been adapted for {new_weekly_hours:.1f} hours/week. "
        f"Life and college exams happen — remaining tasks have been smoothly re-allocated without any penalty."
    )

    history = roadmap.rescheduling_history or []
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "previous_hours": roadmap.weekly_hours,
        "new_hours": new_weekly_hours,
        "reason": reason,
        "explanation": explanation
    })

    roadmap.version += 1
    roadmap.weekly_hours = new_weekly_hours
    roadmap.phases = updated_phases
    roadmap.rescheduling_history = history
    roadmap.missed_tasks_count = 0  # reset after rescheduling
    roadmap.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(roadmap)
    return roadmap
