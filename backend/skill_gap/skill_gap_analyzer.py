import json
import os
import re


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "skill_gap",
    "skill_database.json"
)


# ============================================================
# DATABASE
# ============================================================

def load_skill_database():

    with open(
        DATABASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "js": "javascript",
    "javascript": "javascript",

    "py": "python",
    "python": "python",

    "reactjs": "react",
    "react.js": "react",
    "react": "react",

    "nodejs": "node",
    "node.js": "node",
    "node": "node",

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

    "sql": "sql"
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_skill(skill):

    skill = str(
        skill
    ).lower().strip()

    skill = re.sub(
        r"^[•\-*]\s*",
        "",
        skill
    )

    skill = re.sub(
        r"^[a-z\s]+:\s*",
        "",
        skill
    )

    skill = skill.replace(
        " ",
        ""
    )

    skill = skill.replace(
        "-",
        ""
    )

    skill = skill.replace(
        "_",
        ""
    )

    skill = skill.replace(
        ".",
        ""
    )

    return skill


# ============================================================
# CANONICAL SKILL
# ============================================================

def canonical_skill(skill):

    normalized = normalize_skill(
        skill
    )

    if normalized in SKILL_ALIASES:

        return SKILL_ALIASES[
            normalized
        ]

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


# ============================================================
# CLEAN RESUME SKILLS
# ============================================================

def extract_resume_skills(
    resume_skills
):

    clean_skills = []

    if not resume_skills:
        return clean_skills

    for item in resume_skills:

        if not item:
            continue

        parts = re.split(
            r"[,;|\n]",
            str(item)
        )

        for part in parts:

            part = part.strip()

            if not part:
                continue

            part = re.sub(
                r"^(programming languages|web technologies|databases|tools|concepts|soft skills)\s*:\s*",
                "",
                part,
                flags=re.IGNORECASE
            )

            part = re.sub(
                r"^[•\-*]\s*",
                "",
                part
            )

            if part:
                clean_skills.append(
                    part
                )

    return list(
        dict.fromkeys(
            clean_skills
        )
    )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    resume_skills,
    education,
    year,
    branch
):

    database = load_skill_database()

    education = str(
        education
    ).lower().strip()

    branch = str(
        branch
    ).lower().strip()

    year = str(
        year
    ).lower().strip()

    print("\n========== SKILL GAP ANALYZER ==========")

    print(
        "Education:",
        education
    )

    print(
        "Year:",
        year
    )

    print(
        "Branch:",
        branch
    )

    try:

        required_skills = database[
            education
        ][branch][year]["skills"]

    except KeyError:

        print(
            "DATABASE LOOKUP FAILED"
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

            "skill_gap_score": 0,

            "required_skills": []
        }

    clean_resume_skills = extract_resume_skills(
        resume_skills
    )

    resume_canonical = set()

    for skill in clean_resume_skills:

        canonical = canonical_skill(
            skill
        )

        if canonical:

            resume_canonical.add(
                canonical
            )

    matched_skills = []
    missing_skills = []

    for required in required_skills:

        required_canonical = canonical_skill(
            required
        )

        if required_canonical in resume_canonical:

            matched_skills.append(
                required
            )

        else:

            missing_skills.append(
                required
            )

    total = len(
        required_skills
    )

    if total > 0:

        score = round(
            len(matched_skills)
            / total
            * 100
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
        "Score:",
        score
    )

    print(
        "========================================\n"
    )

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