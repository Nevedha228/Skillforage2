from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import JobPosting, User, UserSkillVerification, CareerRole
from app.core.config import settings

LOW_SAMPLE_THRESHOLD = 25

def get_market_analytics_summary(
    data_origin: str = "synthetic_demo",
    role_filter: Optional[str] = None,
    db: Session = None
) -> Dict[str, Any]:
    query = db.query(JobPosting)

    if data_origin == "all":
        pass  # Query all, but will flag origin
    else:
        query = query.filter(JobPosting.data_origin == data_origin)

    if role_filter:
        query = query.filter(JobPosting.category.ilike(f"%{role_filter}%"))

    postings = query.all()
    total_count = len(postings)

    # Low sample warning
    is_low_sample = total_count < LOW_SAMPLE_THRESHOLD
    low_sample_warning = (
        f"Warning: Sample size ({total_count} postings) is below recommended statistical significance threshold "
        f"({LOW_SAMPLE_THRESHOLD}). Metrics should be treated as indicative."
        if is_low_sample else None
    )

    # 1. Top Skills
    all_skills = []
    for p in postings:
        if p.skills_extracted:
            all_skills.extend(p.skills_extracted)

    skill_counts = Counter(all_skills)
    top_skills = [
        {"skill": skill, "count": count, "percentage": round((count / max(total_count, 1)) * 100, 1)}
        for skill, count in skill_counts.most_common(20)
    ]

    # 2. Role Distribution
    role_counts = Counter(p.category for p in postings if p.category)
    role_distribution = [
        {"role": role, "count": count, "percentage": round((count / max(total_count, 1)) * 100, 1)}
        for role, count in role_counts.most_common(15)
    ]

    # 3. Experience Level Distribution
    exp_counts = Counter(p.experience_level for p in postings if p.experience_level)
    experience_distribution = [
        {"level": lvl.capitalize(), "count": count, "percentage": round((count / max(total_count, 1)) * 100, 1)}
        for lvl, count in exp_counts.items()
    ]

    # 4. Location Distribution
    loc_counts = Counter(p.location.split(",")[0].strip() for p in postings if p.location)
    location_distribution = [
        {"location": loc, "count": count, "percentage": round((count / max(total_count, 1)) * 100, 1)}
        for loc, count in loc_counts.most_common(10)
    ]

    # 5. Salary Analysis by Experience Level
    salary_by_exp = defaultdict(list)
    for p in postings:
        if p.salary_min and p.salary_max and p.experience_level:
            mid = (p.salary_min + p.salary_max) / 2
            salary_by_exp[p.experience_level].append(mid)

    salary_metrics = []
    for lvl, sals in salary_by_exp.items():
        if sals:
            salary_metrics.append({
                "level": lvl.capitalize(),
                "median_salary": round(sorted(sals)[len(sals) // 2]),
                "min_salary": round(min(sals)),
                "max_salary": round(max(sals)),
                "sample_size": len(sals)
            })

    # 6. Posting Trend over Time (by month / week)
    date_counts = Counter()
    dates = []
    for p in postings:
        if p.posted_date:
            dates.append(p.posted_date)
            date_key = p.posted_date.strftime("%Y-%m-%d")
            date_counts[date_key] += 1

    sorted_dates = sorted(date_counts.items())
    trend_data = [{"date": d, "postings": c} for d, c in sorted_dates]

    date_range_str = (
        f"{min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}"
        if dates else "N/A"
    )

    # 7. Skill Co-occurrence (Pairs of skills appearing together)
    co_occurrences = Counter()
    for p in postings:
        skills = sorted(list(set(p.skills_extracted or [])))
        for i in range(len(skills)):
            for j in range(i + 1, min(len(skills), i + 4)):
                pair = f"{skills[i]} + {skills[j]}"
                co_occurrences[pair] += 1

    top_co_occurrences = [
        {"pair": pair, "count": cnt}
        for pair, cnt in co_occurrences.most_common(10)
    ]

    # 8. Source Coverage
    source_counts = Counter(p.source for p in postings)

    return {
        "data_origin": data_origin,
        "is_synthetic": (data_origin == "synthetic_demo"),
        "total_postings": total_count,
        "date_range": date_range_str,
        "low_sample_warning": low_sample_warning,
        "top_skills": top_skills,
        "role_distribution": role_distribution,
        "experience_distribution": experience_distribution,
        "location_distribution": location_distribution,
        "salary_metrics": salary_metrics,
        "trend_data": trend_data,
        "skill_co_occurrences": top_co_occurrences,
        "source_coverage": dict(source_counts),
        "last_updated": datetime.utcnow().isoformat()
    }


def compare_user_skill_gap(
    user_id: int,
    target_role_id: str,
    db: Session
) -> Dict[str, Any]:
    """
    Compares the student's evidenced skills against employer market demand
    for their target role, generating prioritized skill gaps.
    """
    role = db.query(CareerRole).filter(CareerRole.id == target_role_id).first()
    if not role:
        # Fallback to software engineer
        role = db.query(CareerRole).first()

    # Get student verified skills
    user_verifs = db.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == user_id
    ).all()
    user_skill_map = {v.skill_name.lower().strip(): v.status for v in user_verifs}

    # Query job postings for this role to determine empirical demand weight
    postings = db.query(JobPosting).filter(
        JobPosting.category.ilike(f"%{role.category}%")
    ).all()

    market_skill_counts = Counter()
    for p in postings:
        if p.skills_extracted:
            for s in p.skills_extracted:
                market_skill_counts[s] += 1

    total_role_jobs = max(len(postings), 1)

    matched_skills = []
    gaps = []

    # Evaluate all role required skills
    role_skills = role.required_skills or {}
    for skill_name, base_weight in role_skills.items():
        norm_name = skill_name.lower().strip()
        status = user_skill_map.get(norm_name, "Not assessed")
        market_freq = market_skill_counts.get(skill_name, int(base_weight * 5))
        demand_pct = round((market_freq / total_role_jobs) * 100, 1)

        is_evidenced = status in ["Demonstrated", "Strong evidence"]

        item = {
            "skill": skill_name,
            "status": status,
            "importance_weight": base_weight,
            "market_demand_pct": min(100.0, demand_pct),
            "evidence_status": status
        }

        if is_evidenced:
            matched_skills.append(item)
        else:
            # Assign priority: Critical (weight >= 9), High (weight >= 7), Medium (< 7)
            if base_weight >= 9 or demand_pct >= 75:
                priority = "Critical"
            elif base_weight >= 7 or demand_pct >= 50:
                priority = "High"
            else:
                priority = "Medium"

            item["priority"] = priority
            gaps.append(item)

    # Sort gaps by importance weight descending
    gaps.sort(key=lambda x: x["importance_weight"], reverse=True)

    match_percentage = round(
        (len(matched_skills) / max(len(role_skills), 1)) * 100, 1
    )

    return {
        "target_role": role.id,
        "target_role_title": role.title,
        "match_percentage": match_percentage,
        "total_required_skills": len(role_skills),
        "evidenced_skills_count": len(matched_skills),
        "missing_skills_count": len(gaps),
        "matched_skills": matched_skills,
        "prioritized_gaps": gaps,
        "recommendation": (
            f"You possess {len(matched_skills)} of {len(role_skills)} essential skills for {role.title}. "
            f"Focus on the {len([g for g in gaps if g['priority'] == 'Critical'])} critical skills in your roadmap."
        )
    }
