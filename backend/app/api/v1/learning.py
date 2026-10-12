from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, Lesson, UserLearningProgress, UserXPLog, DailyActivity
from app.schemas.learning import (
    LessonListItem,
    LessonDetailResponse,
    ExternalResourceItem,
    QuizQuestionItem,
    QuizSubmitRequest,
    QuizSubmitResponse,
    BookmarkToggleRequest
)

router = APIRouter(prefix="/learning", tags=["Learning Hub"])

@router.get("/lessons", response_model=List[LessonListItem])
def list_lessons(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    bookmarked_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)

    if category:
        query = query.filter(Lesson.skill_category == category)
    if difficulty:
        query = query.filter(Lesson.difficulty == difficulty)

    lessons = query.all()

    # Fetch user progress map
    progress_records = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id
    ).all()
    progress_map = {p.lesson_id: p for p in progress_records}

    results = []
    for l in lessons:
        prog = progress_map.get(l.id)
        is_comp = bool(prog and prog.is_completed)
        is_bm = bool(prog and prog.is_bookmarked)

        if bookmarked_only and not is_bm:
            continue

        results.append(LessonListItem(
            id=l.id,
            skill_category=l.skill_category,
            title=l.title,
            difficulty=l.difficulty,
            estimated_minutes=l.estimated_minutes,
            is_completed=is_comp,
            is_bookmarked=is_bm
        ))

    return results


@router.get("/lessons/{lesson_id}", response_model=LessonDetailResponse)
def get_lesson_detail(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found.")

    prog = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id,
        UserLearningProgress.lesson_id == lesson_id
    ).first()

    # Note: Merely opening a lesson records access timestamp but DOES NOT mark it complete
    if not prog:
        prog = UserLearningProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_completed=False,
            is_bookmarked=False,
            quiz_passed=False,
            last_accessed_at=datetime.utcnow()
        )
        db.add(prog)
        db.commit()
        db.refresh(prog)
    else:
        prog.last_accessed_at = datetime.utcnow()
        db.commit()

    quiz_data = lesson.quiz or {}
    public_quiz = QuizQuestionItem(
        question=quiz_data.get("question", "What is the key takeaway of this lesson?"),
        options=quiz_data.get("options", ["Option A", "Option B", "Option C", "Option D"])
    )

    resources = [
        ExternalResourceItem(title=r.get("title", ""), url=r.get("url", ""), type=r.get("type", "Resource"))
        for r in (lesson.external_resources or [])
    ]

    return LessonDetailResponse(
        id=lesson.id,
        skill_category=lesson.skill_category,
        title=lesson.title,
        difficulty=lesson.difficulty,
        estimated_minutes=lesson.estimated_minutes,
        content_markdown=lesson.content_markdown,
        external_resources=resources,
        quiz=public_quiz,
        is_completed=prog.is_completed,
        is_bookmarked=prog.is_bookmarked,
        quiz_passed=prog.quiz_passed,
        time_spent_minutes=prog.time_spent_minutes
    )


@router.post("/lessons/{lesson_id}/submit-quiz", response_model=QuizSubmitResponse)
def submit_lesson_quiz(
    lesson_id: int,
    req: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates quiz on the backend.
    Lesson counts as complete ONLY after successfully passing this quiz!
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found.")

    prog = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id,
        UserLearningProgress.lesson_id == lesson_id
    ).first()

    if not prog:
        prog = UserLearningProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.add(prog)

    quiz_data = lesson.quiz or {}
    correct_answer = quiz_data.get("correct_answer", "").strip().lower()
    user_answer = req.selected_answer.strip().lower()
    explanation = quiz_data.get("explanation", "Review lesson notes for details.")

    is_correct = (user_answer == correct_answer)

    xp_awarded = 0
    if is_correct:
        prog.quiz_passed = True
        prog.is_completed = True
        prog.completed_at = datetime.utcnow()
        prog.time_spent_minutes += (req.time_spent_minutes or lesson.estimated_minutes)

        # Award XP idempotently
        ref_id = f"lesson_{lesson_id}"
        existing_xp = db.query(UserXPLog).filter(
            UserXPLog.user_id == current_user.id,
            UserXPLog.action_type == "lesson_complete",
            UserXPLog.reference_id == ref_id
        ).first()

        if not existing_xp:
            xp_awarded = 35
            db.add(UserXPLog(
                user_id=current_user.id,
                action_type="lesson_complete",
                reference_id=ref_id,
                xp_amount=xp_awarded,
                created_at=datetime.utcnow()
            ))

            # Record streak activity
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
                    xp_earned=xp_awarded,
                    last_active_at=datetime.utcnow()
                ))
            else:
                daily.actions_count += 1
                daily.xp_earned += xp_awarded
                daily.last_active_at = datetime.utcnow()

        db.commit()
        return QuizSubmitResponse(
            is_correct=True,
            correct_answer=quiz_data.get("correct_answer", ""),
            explanation=explanation,
            lesson_completed=True,
            xp_awarded=xp_awarded,
            message="Quiz passed! Lesson marked as completed."
        )
    else:
        db.commit()
        return QuizSubmitResponse(
            is_correct=False,
            correct_answer=quiz_data.get("correct_answer", ""),
            explanation=explanation,
            lesson_completed=False,
            xp_awarded=0,
            message="Incorrect answer. Review the concept and try again to complete this lesson."
        )


@router.post("/lessons/{lesson_id}/bookmark")
def toggle_bookmark(
    lesson_id: int,
    req: BookmarkToggleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prog = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id,
        UserLearningProgress.lesson_id == lesson_id
    ).first()

    if not prog:
        prog = UserLearningProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_bookmarked=req.is_bookmarked
        )
        db.add(prog)
    else:
        prog.is_bookmarked = req.is_bookmarked

    db.commit()
    return {"success": True, "is_bookmarked": req.is_bookmarked}
