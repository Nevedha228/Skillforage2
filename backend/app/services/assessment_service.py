from typing import List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import (
    AssessmentQuestion,
    UserAssessment,
    UserSkillVerification,
    UserXPLog,
    DailyActivity
)
from app.schemas.assessment import (
    AssessmentStartResponse,
    QuestionPublic,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    TopicScore,
    QuestionReviewItem,
    AssessmentHistoryResponse,
    AssessmentHistoryItem
)

def start_assessment(category: str, difficulty: str, db: Session) -> AssessmentStartResponse:
    questions = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.category == category,
        AssessmentQuestion.difficulty == difficulty
    ).all()

    if not questions:
        # Fallback to category only if difficulty exact match not found
        questions = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.category == category
        ).limit(10).all()

    public_questions = [
        QuestionPublic(
            id=q.id,
            category=q.category,
            difficulty=q.difficulty,
            question_type=q.question_type,
            question_text=q.question_text,
            options=q.options,
            topic_tag=q.topic_tag,
            code_starter=q.code_starter
        )
        for q in questions
    ]

    time_limit = len(public_questions) * 90  # 90 seconds per question

    return AssessmentStartResponse(
        category=category,
        difficulty=difficulty,
        total_questions=len(public_questions),
        time_limit_seconds=time_limit,
        questions=public_questions
    )


def evaluate_assessment_submission(
    req: AssessmentSubmitRequest,
    user_id: int,
    db: Session
) -> AssessmentResultResponse:
    submission_map = {ans.question_id: ans.selected_answer.strip().lower() for ans in req.answers}
    question_ids = list(submission_map.keys())

    db_questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.id.in_(question_ids)).all()
    q_dict = {q.id: q for q in db_questions}

    total_questions = len(db_questions)
    if total_questions == 0:
        total_questions = 1

    correct_count = 0
    topic_stats: Dict[str, Dict[str, int]] = {}
    review_items: List[QuestionReviewItem] = []

    for q in db_questions:
        user_ans = submission_map.get(q.id, "")
        correct_ans = q.correct_answer.strip().lower()
        is_correct = (user_ans == correct_ans)

        if is_correct:
            correct_count += 1

        topic = q.topic_tag or "General Fundamentals"
        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}
        topic_stats[topic]["total"] += 1
        if is_correct:
            topic_stats[topic]["correct"] += 1

        review_items.append(QuestionReviewItem(
            question_id=q.id,
            question_text=q.question_text,
            selected_answer=submission_map.get(q.id, "No answer provided"),
            correct_answer=q.correct_answer,
            is_correct=is_correct,
            explanation=q.explanation,
            topic_tag=q.topic_tag
        ))

    score = float(correct_count)
    max_score = float(total_questions)
    percentage = round((score / max_score) * 100, 1)

    # Classify proficiency level
    if percentage >= 85:
        proficiency = "Advanced"
        verification_status = "Strong evidence"
    elif percentage >= 70:
        proficiency = "Competent"
        verification_status = "Demonstrated"
    elif percentage >= 50:
        proficiency = "Developing"
        verification_status = "In progress"
    else:
        proficiency = "Foundational"
        verification_status = "In progress"

    # Identify weak topics (< 60% accuracy)
    weak_topics: List[str] = []
    topic_breakdown: Dict[str, TopicScore] = {}

    for t, stat in topic_stats.items():
        pct = round((stat["correct"] / stat["total"]) * 100, 1)
        topic_breakdown[t] = TopicScore(
            correct=stat["correct"],
            total=stat["total"],
            percentage=pct
        )
        if pct < 60.0:
            weak_topics.append(t)

    # Generate targeted recommendations
    recommendations: List[str] = []
    if weak_topics:
        for wt in weak_topics[:3]:
            recommendations.append(f"Review core principles of '{wt}' and practice hands-on coding exercises.")
    else:
        recommendations.append(f"Outstanding performance across all topics! Proceed to higher difficulty assessments.")

    if req.time_taken_seconds > (total_questions * 120):
        recommendations.append("Work on solving questions within standard interview time limits.")

    # 1. Persist UserAssessment record
    assessment_record = UserAssessment(
        user_id=user_id,
        category=req.category,
        difficulty=req.difficulty,
        score=score,
        max_score=max_score,
        percentage=percentage,
        time_taken_seconds=req.time_taken_seconds,
        topic_breakdown={k: v.model_dump() for k, v in topic_breakdown.items()},
        weak_topics=weak_topics,
        recommendations=recommendations,
        created_at=datetime.utcnow()
    )
    db.add(assessment_record)
    db.commit()
    db.refresh(assessment_record)

    # 2. Update UserSkillVerification evidence (Never using the word 'certified')
    verif = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == user_id,
        UserSkillVerification.skill_name == req.category
    ).first()

    evidence_entry = {
        "type": "assessment",
        "category": req.category,
        "difficulty": req.difficulty,
        "score_percent": percentage,
        "assessment_id": assessment_record.id,
        "date": datetime.utcnow().isoformat()
    }

    if not verif:
        verif = UserSkillVerification(
            user_id=user_id,
            skill_name=req.category,
            status=verification_status,
            evidence_sources=[evidence_entry],
            last_evaluated_at=datetime.utcnow()
        )
        db.add(verif)
    else:
        # Upgrade status if score is higher
        if verification_status == "Strong evidence":
            verif.status = "Strong evidence"
        elif verification_status == "Demonstrated" and verif.status != "Strong evidence":
            verif.status = "Demonstrated"
        existing_evidence = verif.evidence_sources or []
        existing_evidence.append(evidence_entry)
        verif.evidence_sources = existing_evidence
        verif.last_evaluated_at = datetime.utcnow()

    # 3. Award XP for completing assessment (Idempotent per assessment_id)
    xp_amount = int(percentage * 0.5) + (50 if percentage >= 70 else 20)
    ref_id = f"assessment_{assessment_record.id}"
    existing_xp = db.query(UserXPLog).filter(
        UserXPLog.user_id == user_id,
        UserXPLog.action_type == "assessment_pass",
        UserXPLog.reference_id == ref_id
    ).first()

    if not existing_xp:
        db.add(UserXPLog(
            user_id=user_id,
            action_type="assessment_pass",
            reference_id=ref_id,
            xp_amount=xp_amount,
            created_at=datetime.utcnow()
        ))

    # 4. Record Daily Activity for Streak
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    daily = db.query(DailyActivity).filter(
        DailyActivity.user_id == user_id,
        DailyActivity.date_str == today_str
    ).first()

    if not daily:
        db.add(DailyActivity(
            user_id=user_id,
            date_str=today_str,
            actions_count=1,
            xp_earned=xp_amount,
            last_active_at=datetime.utcnow()
        ))
    else:
        daily.actions_count += 1
        daily.xp_earned += xp_amount
        daily.last_active_at = datetime.utcnow()

    db.commit()

    return AssessmentResultResponse(
        id=assessment_record.id,
        category=req.category,
        difficulty=req.difficulty,
        score=score,
        max_score=max_score,
        percentage=percentage,
        proficiency_level=proficiency,
        time_taken_seconds=req.time_taken_seconds,
        topic_breakdown=topic_breakdown,
        weak_topics=weak_topics,
        recommendations=recommendations,
        verification_status=verification_status,
        review=review_items
    )
