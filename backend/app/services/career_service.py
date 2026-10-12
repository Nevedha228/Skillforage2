from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models import CareerRole
from app.schemas.career import (
    CareerQuestionnaireRequest,
    CareerRoleMatch,
    RoleMatchExplanation,
    CareerDiscoveryResponse
)

HEURISTIC_DISCLAIMER = (
    "Disclaimer: Career match percentages are heuristic algorithmic estimates derived from self-reported "
    "interests, selected skills, and current market skill profiles. They are intended as an educational planning "
    "guide and do not constitute a psychometric test or a guarantee of employment suitability."
)

def calculate_career_matches(req: CareerQuestionnaireRequest, db: Session) -> CareerDiscoveryResponse:
    roles = db.query(CareerRole).all()
    results: List[CareerRoleMatch] = []

    user_interests = set(i.lower().strip() for i in req.interests)
    user_skills = set(s.lower().strip() for s in req.known_skills)
    user_activities = set(a.lower().strip() for a in req.activities)

    for role in roles:
        # 1. Interest Match (Weight: 35%)
        role_interests = set(i.lower().strip() for i in (role.interest_tags or []))
        matched_interests = user_interests.intersection(role_interests)
        interest_score = (len(matched_interests) / max(len(role_interests), 1)) * 100

        # 2. Skill Match (Weight: 45%)
        role_skills_dict = role.required_skills or {}
        total_possible_skill_weight = sum(role_skills_dict.values()) or 1
        matched_skill_weight = 0
        matched_skills_list = []
        missing_skills_list = []

        for skill_name, weight in role_skills_dict.items():
            if skill_name.lower().strip() in user_skills:
                matched_skill_weight += weight
                matched_skills_list.append(skill_name)
            else:
                missing_skills_list.append(skill_name)

        skill_score = (matched_skill_weight / total_possible_skill_weight) * 100

        # 3. Style & Goal Fit (Weight: 20%)
        style_fit = 60.0  # Baseline reasonable fit
        if req.problem_solving_style == "analytical" and role.category in ["Data & Analytics", "Security"]:
            style_fit += 25
        elif req.problem_solving_style == "systematic" and role.category in ["Software Engineering", "Cloud & Infrastructure"]:
            style_fit += 25
        elif req.problem_solving_style == "creative" and role.category in ["Web Development", "Product & Strategy"]:
            style_fit += 25
        style_fit = min(100.0, style_fit)

        # Composite Match Score (0 - 100)
        composite_score = int(round((interest_score * 0.35) + (skill_score * 0.45) + (style_fit * 0.20)))
        composite_score = max(10, min(99, composite_score))

        # Format Explanation
        matching_interest_names = [i for i in (role.interest_tags or []) if i.lower().strip() in user_interests]
        summary_text = (
            f"Matches {len(matching_interest_names)} of your core interests and {len(matched_skills_list)} "
            f"demonstrated skills. Developing {len(missing_skills_list)} key technical competencies will bridge this gap."
        )

        explanation = RoleMatchExplanation(
            matching_interests=matching_interest_names,
            strengths=matched_skills_list,
            missing_skills=missing_skills_list,
            match_breakdown={
                "interest_alignment": round(interest_score, 1),
                "skill_alignment": round(skill_score, 1),
                "workstyle_fit": round(style_fit, 1)
            },
            summary=summary_text
        )

        results.append(CareerRoleMatch(
            id=role.id,
            title=role.title,
            category=role.category,
            description=role.description,
            match_score=composite_score,
            explanation=explanation,
            responsibilities=role.responsibilities or [],
            learning_priorities=role.learning_priorities or [],
            related_roles=role.related_roles or []
        ))

    # Sort descending by match score
    results.sort(key=lambda x: x.match_score, reverse=True)

    return CareerDiscoveryResponse(
        disclaimer=HEURISTIC_DISCLAIMER,
        recommended_roles=results,
        total_evaluated=len(results)
    )
