import json
import os
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "skill_gap",
    "skill_database.json"
)


def load_skill_database():
    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------
# Skill aliases
# ------------------------------------------

SKILL_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",

    "py": "python",

    "reactjs": "react",
    "react.js": "react",

    "nodejs": "node",
    "node.js": "node",

    "springboot": "spring boot",
    "spring boot": "spring boot",

    "restapi": "rest api",
    "rest api": "rest api",

    "oops": "object oriented programming",
    "oop": "object oriented programming",

    "dsa": "data structures",
    "data structures and algorithms": "data structures",
    "data structures": "data structures",

    "mysql": "mysql",
    "mongo": "mongodb",
    "mongodb": "mongodb",

    "github": "github",
    "git": "git",

    "html5": "html",
    "html": "html",

    "css3": "css",
    "css": "css",

    "sql": "sql",
    "java": "java",
    "python": "python"
}


def normalize_skill(skill):
    skill = str(skill).lower().strip()

    # Remove bullets and common labels
    skill = re.sub(
        r"^[•\-*]\s*",
        "",
        skill
    )

    # Remove labels such as:
    # Programming Languages:
    # Web Technologies:
    # Databases:
    # Tools:
    # Concepts:
    skill = re.sub(
        r"^[a-z\s]+:\s*",
        "",
        skill
    )

    skill = skill.replace(" ", "")
    skill = skill.replace("-", "")
    skill = skill.replace("_", "")
    skill = skill.replace(".", "")

    return skill


def canonical_skill(skill):
    normalized = normalize_skill(skill)

    # Direct alias
    if normalized in SKILL_ALIASES:
        return SKILL_ALIASES[normalized]

    # Check aliases after removing spaces
    for key, value in SKILL_ALIASES.items():

        key_normalized = (
            key.lower()
            .replace(" ", "")
            .replace(".", "")
            .replace("-", "")
        )

        if normalized == key_normalized:
            return value

    return normalized


def extract_resume_skills(resume_skills):

    clean_skills = []

    for item in resume_skills:

        if not item:
            continue

        item = str(item)

        # Split things like:
        # Java, Python, SQL
        parts = re.split(
            r"[,;|\n]",
            item
        )

        for part in parts:

            part = part.strip()

            if not part:
                continue

            # Remove category labels
            part = re.sub(
                r"^(programming languages|web technologies|databases|tools|concepts|soft skills)\s*:\s*",
                "",
                part,
                flags=re.IGNORECASE
            )

            # Remove bullets
            part = re.sub(
                r"^[•\-*]\s*",
                "",
                part
            )

            if part:
                clean_skills.append(part)

    return clean_skills


def analyze_skill_gap(
    resume_skills,
    education,
    year,
    branch
):

    database = load_skill_database()

    education = str(education).lower().strip()
    branch = str(branch).lower().strip()
    year = str(year).lower().strip()

    print("\n========== ANALYZER ==========")
    print("Education:", education)
    print("Year:", year)
    print("Branch:", branch)

    # ------------------------------------------
    # Find required skills
    # ------------------------------------------

    try:

        required_skills = database[
            education
        ][branch][year]["skills"]

    except KeyError:

        print("DATABASE LOOKUP FAILED")

        print(
            "Available education:",
            list(database.keys())
        )

        if education in database:
            print(
                "Available branches:",
                list(database[education].keys())
            )

            if branch in database[education]:
                print(
                    "Available years:",
                    list(database[education][branch].keys())
                )

        return {
            "success": False,
            "message": (
                "Roadmap not available for "
                f"education={education}, "
                f"branch={branch}, "
                f"year={year}"
            ),
            "matched_skills": [],
            "missing_skills": [],
            "skill_gap_score": 0
        }

    # ------------------------------------------
    # Clean resume skills
    # ------------------------------------------

    clean_resume_skills = extract_resume_skills(
        resume_skills
    )

    print(
        "Clean Resume Skills:",
        clean_resume_skills
    )

    # ------------------------------------------
    # Create canonical skill set
    # ------------------------------------------

    resume_canonical = set()

    for skill in clean_resume_skills:

        canonical = canonical_skill(skill)

        if canonical:
            resume_canonical.add(canonical)

    print(
        "Canonical Resume Skills:",
        resume_canonical
    )

    # ------------------------------------------
    # Compare required skills
    # ------------------------------------------

    matched_skills = []
    missing_skills = []

    for required in required_skills:

        required_canonical = canonical_skill(
            required
        )

        if required_canonical in resume_canonical:

            matched_skills.append(required)

        else:

            missing_skills.append(required)

    # ------------------------------------------
    # Calculate score
    # ------------------------------------------

    total = len(required_skills)

    if total > 0:

        score = round(
            len(matched_skills) / total * 100
        )

    else:

        score = 0

    print(
        "Matched:",
        matched_skills
    )

    print(
        "Missing:",
        missing_skills
    )

    print(
        "Skill Gap Score:",
        score
    )

    print("==============================\n")

    return {
        "success": True,

        "education": education,

        "branch": branch,

        "year": year,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_gap_score": score,

        "resume_skills": clean_resume_skills
    }