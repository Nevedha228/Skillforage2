import sys
import json
from pathlib import Path
from datetime import datetime

# Add backend root to path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal, init_db
from app.models import (
    CareerRole,
    SkillTaxonomy,
    AssessmentQuestion,
    Lesson,
    JobPosting,
    Challenge,
    ProjectTemplate,
    HackathonEvent
)

DATA_DIR = BACKEND_DIR / "data"

def seed_database():
    print("Initializing tables if not present...")
    init_db()

    db = SessionLocal()
    try:
        print("\n--- Seeding Career Roles ---")
        career_file = DATA_DIR / "career_profiles.json"
        if career_file.exists():
            with open(career_file, "r", encoding="utf-8") as f:
                careers = json.load(f)
            for c in careers:
                existing = db.query(CareerRole).filter(CareerRole.id == c["id"]).first()
                if not existing:
                    db.add(CareerRole(
                        id=c["id"],
                        title=c["title"],
                        category=c["category"],
                        description=c["description"],
                        responsibilities=c.get("responsibilities", []),
                        required_skills=c.get("required_skills", {}),
                        interest_tags=c.get("interest_tags", []),
                        learning_priorities=c.get("learning_priorities", []),
                        related_roles=c.get("related_roles", []),
                        is_demo=c.get("is_demo", False)
                    ))
            db.commit()
            print(f"Seeded/Verified {len(careers)} career roles.")

        print("\n--- Seeding Skills Taxonomy ---")
        skills_file = DATA_DIR / "skills_taxonomy.json"
        if skills_file.exists():
            with open(skills_file, "r", encoding="utf-8") as f:
                skills = json.load(f)
            count = 0
            for s in skills:
                existing = db.query(SkillTaxonomy).filter(SkillTaxonomy.name == s["name"]).first()
                if not existing:
                    db.add(SkillTaxonomy(
                        name=s["name"],
                        category=s["category"],
                        synonyms=s.get("synonyms", []),
                        description=s.get("description", "")
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new skills (taxonomy total verified: {len(skills)}).")

        print("\n--- Seeding Assessment Questions ---")
        questions_file = DATA_DIR / "assessment_questions.json"
        if questions_file.exists():
            with open(questions_file, "r", encoding="utf-8") as f:
                questions = json.load(f)
            count = 0
            for q in questions:
                existing = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.question_text == q["question_text"],
                    AssessmentQuestion.category == q["category"]
                ).first()
                if not existing:
                    db.add(AssessmentQuestion(
                        category=q["category"],
                        difficulty=q["difficulty"],
                        question_type=q.get("question_type", "multiple_choice"),
                        question_text=q["question_text"],
                        options=q.get("options", []),
                        correct_answer=q["correct_answer"],
                        topic_tag=q["topic_tag"],
                        explanation=q["explanation"],
                        code_starter=q.get("code_starter"),
                        test_cases_or_rubric=q.get("test_cases_or_rubric")
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new questions (total verified: {len(questions)}).")

        print("\n--- Seeding Lessons ---")
        lessons_file = DATA_DIR / "lessons.json"
        if lessons_file.exists():
            with open(lessons_file, "r", encoding="utf-8") as f:
                lessons = json.load(f)
            count = 0
            for l in lessons:
                existing = db.query(Lesson).filter(
                    Lesson.title == l["title"],
                    Lesson.skill_category == l["skill_category"]
                ).first()
                if not existing:
                    db.add(Lesson(
                        skill_category=l["skill_category"],
                        title=l["title"],
                        difficulty=l["difficulty"],
                        content_markdown=l["content_markdown"],
                        estimated_minutes=l.get("estimated_minutes", 15),
                        external_resources=l.get("external_resources", []),
                        quiz=l.get("quiz", {}),
                        is_demo=l.get("is_demo", False)
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new lessons (total verified: {len(lessons)}).")

        print("\n--- Seeding Market Job Postings ---")
        jobs_file = DATA_DIR / "market_seed_jobs.json"
        if jobs_file.exists():
            with open(jobs_file, "r", encoding="utf-8") as f:
                jobs = json.load(f)
            count = 0
            for j in jobs:
                existing = db.query(JobPosting).filter(
                    JobPosting.source_job_id == j["source_job_id"]
                ).first()
                if not existing:
                    posted_date = None
                    if j.get("posted_date"):
                        try:
                            posted_date = datetime.fromisoformat(j["posted_date"])
                        except Exception:
                            posted_date = None

                    db.add(JobPosting(
                        source=j["source"],
                        source_job_id=j["source_job_id"],
                        title=j["title"],
                        company=j["company"],
                        location=j["location"],
                        description=j["description"],
                        url=j.get("url"),
                        category=j["category"],
                        salary_min=j.get("salary_min"),
                        salary_max=j.get("salary_max"),
                        experience_level=j.get("experience_level", "entry"),
                        skills_extracted=j.get("skills_extracted", []),
                        is_demo=j.get("is_demo", True),
                        data_origin=j.get("data_origin", "synthetic_demo"),
                        posted_date=posted_date
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new job postings (total verified: {len(jobs)}).")

        print("\n--- Seeding Challenges ---")
        challenges_file = DATA_DIR / "challenges.json"
        if challenges_file.exists():
            with open(challenges_file, "r", encoding="utf-8") as f:
                challenges = json.load(f)
            count = 0
            for ch in challenges:
                existing = db.query(Challenge).filter(Challenge.title == ch["title"]).first()
                if not existing:
                    db.add(Challenge(
                        title=ch["title"],
                        challenge_type=ch["challenge_type"],
                        skill_category=ch["skill_category"],
                        description=ch["description"],
                        hints=ch.get("hints", []),
                        xp_reward=ch.get("xp_reward", 50),
                        solution_type=ch.get("solution_type", "quiz"),
                        verification_rules=ch.get("verification_rules", {}),
                        is_active=ch.get("is_active", True)
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new challenges (total verified: {len(challenges)}).")

        print("\n--- Seeding Project Templates ---")
        projects_file = DATA_DIR / "project_templates.json"
        if projects_file.exists():
            with open(projects_file, "r", encoding="utf-8") as f:
                projects = json.load(f)
            count = 0
            for p in projects:
                existing = db.query(ProjectTemplate).filter(ProjectTemplate.title == p["title"]).first()
                if not existing:
                    db.add(ProjectTemplate(
                        title=p["title"],
                        target_role=p["target_role"],
                        difficulty=p["difficulty"],
                        year_suitability=p.get("year_suitability", [1, 2, 3, 4]),
                        problem_statement=p["problem_statement"],
                        relevance=p["relevance"],
                        skills=p.get("skills", []),
                        duration_hours=p.get("duration_hours", 20),
                        milestones=p.get("milestones", []),
                        architecture=p["architecture"],
                        datasets=p.get("datasets", []),
                        deliverables=p.get("deliverables", []),
                        evaluation_checklist=p.get("evaluation_checklist", []),
                        extensions=p.get("extensions", [])
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new project templates (total verified: {len(projects)}).")

        print("\n--- Seeding Hackathon Events ---")
        hackathons_file = DATA_DIR / "hackathons.json"
        if hackathons_file.exists():
            with open(hackathons_file, "r", encoding="utf-8") as f:
                hackathons = json.load(f)
            count = 0
            for h in hackathons:
                existing = db.query(HackathonEvent).filter(HackathonEvent.name == h["name"]).first()
                if not existing:
                    db.add(HackathonEvent(
                        name=h["name"],
                        organizer=h["organizer"],
                        mode=h.get("mode", "online"),
                        location=h.get("location", "Virtual"),
                        date=h["date"],
                        deadline=h["deadline"],
                        eligibility=h.get("eligibility", "College Students"),
                        description=h["description"],
                        official_link=h["official_link"],
                        source=h.get("source", "Demo Entry"),
                        last_verified=h.get("last_verified", "2026-10-11"),
                        is_demo=h.get("is_demo", True)
                    ))
                    count += 1
            db.commit()
            print(f"Seeded {count} new hackathon events (total verified: {len(hackathons)}).")

        print("\nDatabase seeding completed successfully and idempotently!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
