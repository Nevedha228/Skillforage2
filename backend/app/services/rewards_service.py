from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import (
    User,
    UserXPLog,
    DailyActivity,
    UserAssessment,
    UserProject,
    UserLearningProgress,
    InterviewSession
)
from app.schemas.challenge import RewardsProfileResponse, BadgeItem

LEVELS = [
    (1, 0, 200, "Novice Explorer"),
    (2, 200, 500, "Apprentice Coder"),
    (3, 500, 1000, "Proficient Builder"),
    (4, 1000, 2000, "Advanced Practitioner"),
    (5, 2000, 4000, "Interview-Ready Specialist"),
    (6, 4000, 10000, "Master Engineer")
]

def calculate_user_rewards(user: User, db: Session) -> RewardsProfileResponse:
    # 1. Total XP from immutable log
    xp_sum = db.query(func.sum(UserXPLog.xp_amount)).filter(UserXPLog.user_id == user.id).scalar() or 0

    # 2. Level calculation
    current_level = 1
    level_title = LEVELS[0][3]
    next_level_xp = LEVELS[0][2]
    progress_pct = 0.0

    for lvl, low, high, title in LEVELS:
        if xp_sum >= low:
            current_level = lvl
            level_title = title
            next_level_xp = high
            span = high - low
            current_span = xp_sum - low
            progress_pct = round(min(100.0, (current_span / span) * 100), 1)

    # 3. Streaks calculation from DailyActivity
    activities = db.query(DailyActivity).filter(
        DailyActivity.user_id == user.id
    ).order_by(DailyActivity.date_str.asc()).all()

    active_dates = sorted(list(set(a.date_str for a in activities)))

    # Compute longest streak
    longest_streak = 0
    current_consecutive = 0
    prev_date = None

    for d_str in active_dates:
        curr_d = datetime.strptime(d_str, "%Y-%m-%d").date()
        if prev_date is None:
            current_consecutive = 1
        elif (curr_d - prev_date).days == 1:
            current_consecutive += 1
        else:
            current_consecutive = 1
        prev_date = curr_d
        if current_consecutive > longest_streak:
            longest_streak = current_consecutive

    # Compute current active streak ending today or yesterday
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    current_streak = 0
    if active_dates:
        latest_date = datetime.strptime(active_dates[-1], "%Y-%m-%d").date()
        if latest_date in (today, yesterday):
            # Walk backwards
            check_date = latest_date
            date_set = set(active_dates)
            while check_date.strftime("%Y-%m-%d") in date_set:
                current_streak += 1
                check_date -= timedelta(days=1)

    # 4. Weekly Activity (Last 7 days)
    activity_map = {a.date_str: a for a in activities}
    weekly_activity = []
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for i in range(6, -1, -1):
        target_day = today - timedelta(days=i)
        target_str = target_day.strftime("%Y-%m-%d")
        record = activity_map.get(target_str)

        weekly_activity.append({
            "day": day_names[target_day.weekday()],
            "date": target_str,
            "active": (record is not None),
            "xp": record.xp_earned if record else 0,
            "actions": record.actions_count if record else 0
        })

    # 5. Badges
    badges: List[BadgeItem] = []

    # First Assessment badge
    has_assessment = db.query(UserAssessment).filter(UserAssessment.user_id == user.id).first()
    if has_assessment:
        badges.append(BadgeItem(
            id="badge_first_assessment",
            name="First Benchmark",
            description="Completed your first comprehensive Skill Assessment.",
            icon="🎯",
            unlocked_at=has_assessment.created_at.strftime("%Y-%m-%d")
        ))

    # Fast Learner badge (>= 3 lessons completed)
    completed_lessons = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == user.id,
        UserLearningProgress.is_completed == True
    ).count()
    if completed_lessons >= 3:
        badges.append(BadgeItem(
            id="badge_fast_learner",
            name="Curious Scholar",
            description="Successfully completed 3 or more technical lessons and quizzes.",
            icon="📚",
            unlocked_at=datetime.utcnow().strftime("%Y-%m-%d")
        ))

    # Streak badge
    if longest_streak >= 3:
        badges.append(BadgeItem(
            id="badge_consistency_streak",
            name="Consistent Pacer",
            description="Maintained a learning streak of 3 or more consecutive days.",
            icon="🔥",
            unlocked_at=datetime.utcnow().strftime("%Y-%m-%d")
        ))

    # Project Builder badge
    has_project = db.query(UserProject).filter(UserProject.user_id == user.id).first()
    if has_project:
        badges.append(BadgeItem(
            id="badge_project_builder",
            name="Portfolio Architect",
            description="Initiated or published a portfolio project.",
            icon="🛠️",
            unlocked_at=has_project.created_at.strftime("%Y-%m-%d")
        ))

    # Interview Ready badge
    has_interview = db.query(InterviewSession).filter(InterviewSession.user_id == user.id).first()
    if has_interview:
        badges.append(BadgeItem(
            id="badge_interview_ready",
            name="Interview Contender",
            description="Completed a full rubric-evaluated mock interview session.",
            icon="🎤",
            unlocked_at=has_interview.created_at.strftime("%Y-%m-%d")
        ))

    next_milestone = f"Reach {next_level_xp} XP to unlock Level {current_level + 1} ({LEVELS[min(len(LEVELS)-1, current_level)][3]})"

    return RewardsProfileResponse(
        total_xp=xp_sum,
        current_level=current_level,
        level_title=level_title,
        next_level_xp=next_level_xp,
        level_progress_percentage=progress_pct,
        current_streak_days=current_streak,
        longest_streak_days=longest_streak,
        weekly_activity=weekly_activity,
        recent_badges=badges,
        next_milestone=next_milestone
    )
