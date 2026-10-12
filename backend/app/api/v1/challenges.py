from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, Challenge, UserChallenge, UserXPLog, DailyActivity
from app.schemas.challenge import (
    ChallengeItem,
    ChallengeSubmitRequest,
    ChallengeSubmitResponse
)

router = APIRouter(prefix="/challenges", tags=["Challenges"])

@router.get("", response_model=List[ChallengeItem])
def list_challenges(
    challenge_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Challenge).filter(Challenge.is_active == True)
    if challenge_type:
        query = query.filter(Challenge.challenge_type == challenge_type)

    challenges = query.all()

    # User completed challenges
    completed_ids = set(
        c.challenge_id
        for c in db.query(UserChallenge).filter(UserChallenge.user_id == current_user.id).all()
    )

    return [
        ChallengeItem(
            id=ch.id,
            title=ch.title,
            challenge_type=ch.challenge_type,
            skill_category=ch.skill_category,
            description=ch.description,
            hints=ch.hints or [],
            xp_reward=ch.xp_reward,
            solution_type=ch.solution_type,
            is_completed=(ch.id in completed_ids)
        )
        for ch in challenges
    ]


@router.post("/{challenge_id}/submit", response_model=ChallengeSubmitResponse)
def submit_challenge(
    challenge_id: int,
    req: ChallengeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found.")

    sub_text = req.submission_text.strip()
    if len(sub_text) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please submit a meaningful solution.")

    # Idempotent: check if already solved
    existing_user_ch = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_id
    ).first()

    if existing_user_ch:
        total_xp = db.query(func.sum(UserXPLog.xp_amount)).filter(UserXPLog.user_id == current_user.id).scalar() or 0
        return ChallengeSubmitResponse(
            is_valid=True,
            message="Challenge was already completed! XP is only awarded once.",
            xp_awarded=0,
            total_user_xp=total_xp
        )

    # Basic keyword validation from verification_rules
    rules = challenge.verification_rules or {}
    keywords = rules.get("keywords") or rules.get("keyword_check") or []
    if keywords:
        for kw in keywords:
            if kw.lower() not in sub_text.lower():
                return ChallengeSubmitResponse(
                    is_valid=False,
                    message=f"Missing key approach or keyword: '{kw}'. Check the hints and refine your solution.",
                    xp_awarded=0,
                    total_user_xp=0
                )

    # Record UserChallenge
    db.add(UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id,
        completed_at=datetime.utcnow()
    ))

    # Award XP server-side (unique constraint on user_id, action_type, reference_id guarantees single payment)
    ref_id = f"challenge_{challenge_id}"
    db.add(UserXPLog(
        user_id=current_user.id,
        action_type="challenge_completion",
        reference_id=ref_id,
        xp_amount=challenge.xp_reward,
        created_at=datetime.utcnow()
    ))

    # Record DailyActivity for streak
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
            xp_earned=challenge.xp_reward,
            last_active_at=datetime.utcnow()
        ))
    else:
        daily.actions_count += 1
        daily.xp_earned += challenge.xp_reward
        daily.last_active_at = datetime.utcnow()

    db.commit()

    total_xp = db.query(func.sum(UserXPLog.xp_amount)).filter(UserXPLog.user_id == current_user.id).scalar() or 0

    return ChallengeSubmitResponse(
        is_valid=True,
        message=f"Challenge solved! +{challenge.xp_reward} XP awarded.",
        xp_awarded=challenge.xp_reward,
        total_user_xp=total_xp
    )
