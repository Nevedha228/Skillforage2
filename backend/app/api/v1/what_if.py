from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, CareerRole, UserSkillVerification
from app.schemas.what_if import (
    WhatIfSimulateRequest,
    WhatIfSimulateResponse,
    ScenarioResult,
    ScenarioParameters,
    WHAT_IF_DISCLAIMER
)

router = APIRouter(prefix="/what-if", tags=["What-If Career Simulator"])

def _simulate_single_scenario(
    params: ScenarioParameters,
    current_user: User,
    db: Session
) -> ScenarioResult:
    role_id = params.target_role or current_user.target_role or "sde"
    role = db.query(CareerRole).filter(CareerRole.id == role_id).first()
    if not role:
        role = db.query(CareerRole).first()

    # User currently evidenced skills
    user_verifs = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == current_user.id
    ).all()
    evidenced_skills = set(v.skill_name.lower().strip() for v in user_verifs if v.status in ["Demonstrated", "Strong evidence"])

    # Add scenario skills
    simulated_skills = evidenced_skills.union(set(s.lower().strip() for s in params.additional_skills))

    # Calculate projected skill coverage
    role_skills = role.required_skills or {}
    total_role_weight = sum(role_skills.values()) or 1
    matched_weight = sum(
        weight for skill, weight in role_skills.items()
        if skill.lower().strip() in simulated_skills
    )
    skill_coverage = round((matched_weight / total_role_weight) * 100, 1)

    # Calculate total study hours over the duration
    total_days = params.months_until_placement * 30
    total_study_hours = round(params.daily_hours * total_days, 1)
    weekly_pace = round(params.daily_hours * 7, 1)

    # Readiness score incorporates skill coverage, study depth, and project output
    project_boost = min(15.0, params.projects_to_complete * 5.0)
    readiness = min(96.0, round((skill_coverage * 0.70) + project_boost + min(15.0, (total_study_hours / 20.0)), 1))

    # Milestones
    timeline = [
        {"month": 1, "focus": "Foundations & First Technical Gap", "expected_hours": int(params.daily_hours * 30)},
        {"month": max(1, params.months_until_placement // 2), "focus": "Portfolio Project & Intermediate Algorithms", "expected_hours": int(params.daily_hours * 30 * (params.months_until_placement // 2))},
        {"month": params.months_until_placement, "focus": "Interview Simulation & Final Readiness", "expected_hours": int(total_study_hours)}
    ]

    advantages = []
    tradeoffs = []

    if params.daily_hours >= 3.0:
        advantages.append(f"High daily intensity ({params.daily_hours}h/day) accelerates skill acquisition rapidly.")
        tradeoffs.append("Risk of academic burnout; ensure regular rest intervals.")
    elif params.daily_hours <= 1.0:
        advantages.append("Highly sustainable and balances easily with college semester courses.")
        tradeoffs.append("Gradual pacing requires starting well ahead of campus placement drives.")

    if params.projects_to_complete >= 2:
        advantages.append(f"Completing {params.projects_to_complete} projects provides strong portfolio evidence for recruiters.")

    if skill_coverage >= 75:
        advantages.append(f"Achieves strong market alignment ({skill_coverage}%) for {role.title}.")
    else:
        tradeoffs.append(f"Leaves some secondary gaps for {role.title} that may require interview discussion.")

    return ScenarioResult(
        name=params.name,
        projected_skill_coverage_pct=skill_coverage,
        projected_readiness_pct=readiness,
        total_study_hours=total_study_hours,
        estimated_weekly_pace=weekly_pace,
        milestone_timeline=timeline,
        key_advantages=advantages,
        tradeoffs_and_risks=tradeoffs
    )


@router.post("/simulate", response_model=WhatIfSimulateResponse)
def simulate_career_scenarios(
    req: WhatIfSimulateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    res_a = _simulate_single_scenario(req.scenario_a, current_user, db)
    res_b = _simulate_single_scenario(req.scenario_b, current_user, db) if req.scenario_b else None

    summary = (
        f"Scenario A achieves {res_a.projected_readiness_pct}% readiness with {res_a.total_study_hours} total hours."
    )
    if res_b:
        diff_readiness = round(res_b.projected_readiness_pct - res_a.projected_readiness_pct, 1)
        diff_hours = round(res_b.total_study_hours - res_a.total_study_hours, 1)
        if diff_readiness > 0:
            summary += f" Scenario B offers a +{diff_readiness}% readiness advantage with {diff_hours:+g} hours invested."
        elif diff_readiness < 0:
            summary += f" Scenario A offers a +{-diff_readiness}% higher readiness compared to Scenario B."
        else:
            summary += " Both scenarios project comparable final interview readiness."

    return WhatIfSimulateResponse(
        disclaimer=WHAT_IF_DISCLAIMER,
        scenario_a_result=res_a,
        scenario_b_result=res_b,
        comparative_summary=summary
    )
