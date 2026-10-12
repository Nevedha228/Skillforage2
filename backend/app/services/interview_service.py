from typing import List, Dict, Any, Tuple
from datetime import datetime
import secrets
from sqlalchemy.orm import Session

from app.models import InterviewSession, UserXPLog, DailyActivity
from app.core.config import settings
from app.schemas.interview import (
    InterviewQuestion,
    InterviewStartResponse,
    InterviewSubmitRequest,
    InterviewSubmitResponse,
    RubricBreakdown,
    InterviewFeedback
)

INTERVIEW_DISCLAIMER = (
    "Disclaimer: This mock interview simulator provides automated rubric feedback based on keyword coverage, "
    "structural heuristics, and software engineering principles. It is designed for educational practice and "
    "does not predict or guarantee performance in real commercial employment interviews."
)

INTERVIEW_QUESTION_BANK = {
    "technical": [
        InterviewQuestion(
            id=1,
            question="Explain the difference between process and thread, and how concurrency is managed in your primary language.",
            category="Operating Systems & Concurrency",
            key_aspects=["memory space", "virtual memory", "threads share memory", "process isolation", "gil or mutex"]
        ),
        InterviewQuestion(
            id=2,
            question="How would you design a relational database schema for an e-commerce platform handling orders and products?",
            category="Database Design",
            key_aspects=["normalization", "primary key", "foreign key", "junction table", "indexes", "transactions"]
        ),
        InterviewQuestion(
            id=3,
            question="Describe how hash maps work internally and how collisions are resolved.",
            category="Data Structures",
            key_aspects=["hash function", "modulo array size", "chaining with linked lists", "open addressing", "amortized o(1)"]
        )
    ],
    "behavioral": [
        InterviewQuestion(
            id=101,
            question="Tell me about a challenging technical project you worked on. What was your role, and how did you resolve conflicts or blockers?",
            category="Behavioral (STAR Method)",
            key_aspects=["situation", "task", "action", "result", "communication", "learnings"]
        ),
        InterviewQuestion(
            id=102,
            question="Describe a situation where you had to learn a completely new technology or framework under a tight deadline.",
            category="Adaptability",
            key_aspects=["deadline", "documentation", "rapid prototyping", "delivery", "outcome"]
        )
    ],
    "sql": [
        InterviewQuestion(
            id=201,
            question="Explain when you would choose an INNER JOIN versus a LEFT JOIN, and how NULL values affect aggregate functions like COUNT().",
            category="SQL & Data Integrity",
            key_aspects=["inner join matches both", "left join preserves left table", "count(column) ignores null", "count(*) counts all rows"]
        ),
        InterviewQuestion(
            id=202,
            question="What are window functions in SQL, and how would you use ROW_NUMBER() to eliminate duplicate records?",
            category="SQL Advanced",
            key_aspects=["partition by", "order by", "cte", "row_number", "where rnk = 1"]
        )
    ],
    "programming": [
        InterviewQuestion(
            id=301,
            question="Walk through your thought process for detecting whether a singly linked list contains a cycle without extra memory.",
            category="Algorithms",
            key_aspects=["floyd cycle detection", "slow pointer", "fast pointer", "intersection", "o(1) space"]
        ),
        InterviewQuestion(
            id=302,
            question="Explain how garbage collection works in modern managed runtimes (like Python or Java JVM).",
            category="Memory Management",
            key_aspects=["reference counting", "mark and sweep", "generational gc", "cyclic references", "stop the world"]
        )
    ],
    "project": [
        InterviewQuestion(
            id=401,
            question="Explain the high-level architecture of your most recent full-stack or data project. What architectural tradeoffs did you make?",
            category="System Architecture",
            key_aspects=["frontend", "backend", "database", "tradeoffs", "scalability", "deployment"]
        )
    ],
    "hr": [
        InterviewQuestion(
            id=501,
            question="Why are you interested in this role and what are your long-term career aspirations for the next 2-3 years?",
            category="Career Alignment",
            key_aspects=["passion for domain", "learning progression", "impact", "continuous improvement"]
        )
    ]
}

def start_interview_session(
    target_role: str,
    interview_type: str,
    difficulty: str
) -> InterviewStartResponse:
    q_type = interview_type.lower()
    questions = INTERVIEW_QUESTION_BANK.get(q_type, INTERVIEW_QUESTION_BANK["technical"])

    session_id = secrets.token_hex(8)

    return InterviewStartResponse(
        session_id=session_id,
        target_role=target_role,
        interview_type=interview_type,
        difficulty=difficulty,
        questions=questions,
        time_limit_minutes=len(questions) * 5,
        disclaimer=INTERVIEW_DISCLAIMER
    )


def evaluate_interview_rubric(
    req: InterviewSubmitRequest,
    user_id: int,
    db: Session
) -> InterviewSubmitResponse:
    answers = req.answers
    total_answers = len(answers) or 1

    total_correctness = 0.0
    total_clarity = 0.0
    total_completeness = 0.0
    total_approach = 0.0
    total_structure = 0.0
    total_comm = 0.0

    strengths = []
    improvements = []

    for ans in answers:
        text = ans.answer_text.strip().lower()
        word_count = len(text.split())

        # Completeness based on depth (target >= 60 words for detailed response)
        if word_count >= 80:
            comp_score = 90.0
        elif word_count >= 50:
            comp_score = 75.0
        elif word_count >= 25:
            comp_score = 55.0
        else:
            comp_score = 30.0

        # Structure & STAR / points detection
        has_structure = any(token in text for token in ["first", "second", "situation", "task", "action", "result", "because", "therefore", "for example"])
        struct_score = 85.0 if has_structure else 60.0

        # Clarity
        clarity_score = 80.0 if (word_count >= 30 and len(text) / max(word_count, 1) < 10) else 65.0

        # Technical / approach keywords
        tech_keywords = ["memory", "time complexity", "o(1)", "o(n)", "index", "scale", "performance", "tradeoff", "user", "api", "database", "test"]
        matched_kws = [k for k in tech_keywords if k in text]
        approach_score = min(95.0, 50.0 + len(matched_kws) * 10)
        correctness_score = min(95.0, 55.0 + len(matched_kws) * 8 + (20 if word_count >= 60 else 0))

        comm_score = 80.0 if not any(filler in text for filler in ["um", "uh", "idk", "stuff", "whatever"]) else 60.0

        total_correctness += correctness_score
        total_clarity += clarity_score
        total_completeness += comp_score
        total_approach += approach_score
        total_structure += struct_score
        total_comm += comm_score

        if matched_kws:
            strengths.append(f"Demonstrated technical reasoning citing '{', '.join(matched_kws[:2])}' in Question {ans.question_id}.")
        if word_count < 40:
            improvements.append(f"Elaborate further on Question {ans.question_id} by sharing real concrete examples or tradeoffs.")

    avg_correctness = round(total_correctness / total_answers, 1)
    avg_clarity = round(total_clarity / total_answers, 1)
    avg_completeness = round(total_completeness / total_answers, 1)
    avg_approach = round(total_approach / total_answers, 1)
    avg_structure = round(total_structure / total_answers, 1)
    avg_comm = round(total_comm / total_answers, 1)

    composite_pct = round(
        (avg_correctness * 0.30) +
        (avg_clarity * 0.15) +
        (avg_completeness * 0.15) +
        (avg_approach * 0.15) +
        (avg_structure * 0.15) +
        (avg_comm * 0.10),
        1
    )

    if not strengths:
        strengths = ["Clear and direct answers provided.", "Addressed the foundational requirements of each interview prompt."]
    if not improvements:
        improvements = ["Add specific quantitative metrics (e.g. latency reduced, rows handled) to strengthen impact."]

    recommendations = [
        "Structure behavioral responses explicitly with Situation, Task, Action, and Measurable Result (STAR).",
        "State Big-O time and space complexity explicitly when discussing algorithms and database queries."
    ]

    rubric_obj = RubricBreakdown(
        correctness=avg_correctness,
        clarity=avg_clarity,
        completeness=avg_completeness,
        approach=avg_approach,
        structure=avg_structure,
        communication=avg_comm,
        total_percentage=composite_pct
    )

    # Status of LLM
    llm_status = "ai_evaluated" if settings.LLM_API_KEY else "heuristic_rubric_fallback"

    feedback_obj = InterviewFeedback(
        strengths=strengths[:3],
        areas_for_improvement=improvements[:3],
        recommendations=recommendations,
        llm_status=llm_status
    )

    # Persist InterviewSession
    session_record = InterviewSession(
        user_id=user_id,
        target_role=req.target_role,
        interview_type=req.interview_type,
        difficulty=req.difficulty,
        questions_and_answers=[a.model_dump() for a in req.answers],
        rubric_scores=rubric_obj.model_dump(),
        feedback=feedback_obj.model_dump(),
        time_taken_seconds=req.time_taken_seconds,
        created_at=datetime.utcnow()
    )
    db.add(session_record)

    # Award XP for interview practice (75 XP)
    ref_id = f"interview_session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{user_id}"
    db.add(UserXPLog(
        user_id=user_id,
        action_type="interview_practice",
        reference_id=ref_id,
        xp_amount=75,
        created_at=datetime.utcnow()
    ))

    # Daily activity
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
            xp_earned=75,
            last_active_at=datetime.utcnow()
        ))
    else:
        daily.actions_count += 1
        daily.xp_earned += 75
        daily.last_active_at = datetime.utcnow()

    db.commit()
    db.refresh(session_record)

    return InterviewSubmitResponse(
        id=session_record.id,
        target_role=req.target_role,
        interview_type=req.interview_type,
        difficulty=req.difficulty,
        time_taken_seconds=req.time_taken_seconds,
        rubric_scores=rubric_obj,
        feedback=feedback_obj,
        disclaimer=INTERVIEW_DISCLAIMER,
        created_at=session_record.created_at
    )
