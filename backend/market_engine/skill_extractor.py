import re
from collections import defaultdict


# ============================================================
# SKILL TAXONOMY
# ============================================================
#
# Format:
#
# "Standard Skill": [
#     "variation 1",
#     "variation 2",
#     ...
# ]
#
# The standard skill name is what SkillForage stores
# and displays in market analysis.
# ============================================================


SKILL_TAXONOMY = {

    # ========================================================
    # DATA ANALYTICS
    # ========================================================

    "SQL": [
        "sql",
        "structured query language",
    ],

    "Python": [
        "python",
        "python3",
        "python 3",
    ],

    "R": [
        "r programming",
        "r language",
        "r programming language",
    ],

    "Excel": [
        "excel",
        "microsoft excel",
        "ms excel",
        "advanced excel",
    ],

    "Power BI": [
        "power bi",
        "powerbi",
        "microsoft power bi",
    ],

    "Tableau": [
        "tableau",
    ],

    "Statistics": [
        "statistics",
        "statistical analysis",
        "statistical modeling",
        "statistical modelling",
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation",
        "data viz",
    ],

    "Pandas": [
        "pandas",
    ],

    "NumPy": [
        "numpy",
    ],


    # ========================================================
    # AI / MACHINE LEARNING
    # ========================================================

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml",
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning",
    ],

    "Natural Language Processing": [
        "natural language processing",
        "nlp",
    ],

    "Computer Vision": [
        "computer vision",
    ],

    "TensorFlow": [
        "tensorflow",
    ],

    "PyTorch": [
        "pytorch",
    ],

    "Scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
    ],


    # ========================================================
    # PROGRAMMING
    # ========================================================

    "Java": [
        "java",
    ],

    "C": [
        "c programming",
        "c language",
        "programming in c",
    ],

    "C++": [
        "c++",
        "cpp",
        "c plus plus",
    ],

    "C#": [
        "c#",
        "c sharp",
    ],

    "JavaScript": [
        "javascript",
        "java script",
        "js",
    ],

    "TypeScript": [
        "typescript",
        "type script",
    ],


    # ========================================================
    # WEB DEVELOPMENT
    # ========================================================

    "HTML": [
        "html",
        "html5",
    ],

    "CSS": [
        "css",
        "css3",
    ],

    "React": [
        "react",
        "react.js",
        "reactjs",
        "react js",
    ],

    "Angular": [
        "angular",
        "angularjs",
        "angular js",
    ],

    "Vue.js": [
        "vue",
        "vue.js",
        "vuejs",
        "vue js",
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node js",
    ],

    "Django": [
        "django",
    ],

    "Flask": [
        "flask",
    ],

    "FastAPI": [
        "fastapi",
        "fast api",
    ],

    "REST API": [
        "rest api",
        "restful api",
        "rest services",
        "restful services",
    ],


    # ========================================================
    # DATABASES
    # ========================================================

    "MySQL": [
        "mysql",
        "my sql",
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres",
        "postgre sql",
    ],

    "MongoDB": [
        "mongodb",
        "mongo db",
    ],

    "Oracle Database": [
        "oracle database",
        "oracle db",
    ],

    "Redis": [
        "redis",
    ],


    # ========================================================
    # CLOUD
    # ========================================================

    "AWS": [
        "aws",
        "amazon web services",
    ],

    "Microsoft Azure": [
        "azure",
        "microsoft azure",
    ],

    "Google Cloud": [
        "google cloud",
        "gcp",
        "google cloud platform",
    ],


    # ========================================================
    # DEVOPS
    # ========================================================

    "Docker": [
        "docker",
        "containerization",
        "containerisation",
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s",
    ],

    "Git": [
        "git",
        "version control",
    ],

    "GitHub": [
        "github",
    ],

    "Jenkins": [
        "jenkins",
    ],

    "CI/CD": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous deployment",
        "continuous delivery",
    ],


    # ========================================================
    # CORE COMPUTER SCIENCE
    # ========================================================

    "Data Structures": [
        "data structures",
        "data structure",
        "dsa",
        "data structures and algorithms",
    ],

    "Algorithms": [
        "algorithms",
        "algorithm",
        "algorithm design",
    ],

    "Object-Oriented Programming": [
        "object oriented programming",
        "object-oriented programming",
        "oops",
        "oop",
        "object oriented design",
    ],

    "DBMS": [
        "dbms",
        "database management systems",
        "database management system",
    ],

    "Operating Systems": [
        "operating systems",
        "operating system",
        "os concepts",
    ],

    "Computer Networks": [
        "computer networks",
        "computer networking",
        "networking concepts",
    ],


    # ========================================================
    # BUSINESS / OTHER
    # ========================================================

    "PowerPoint": [
        "powerpoint",
        "power point",
        "microsoft powerpoint",
    ],

    "Communication": [
        "communication skills",
        "communication",
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving",
    ],
}


# ============================================================
# SKILL CATEGORIES
# ============================================================

SKILL_CATEGORIES = {

    "Data Analytics": {
        "SQL",
        "Python",
        "R",
        "Excel",
        "Power BI",
        "Tableau",
        "Statistics",
        "Data Visualization",
        "Pandas",
        "NumPy",
    },

    "AI / Machine Learning": {
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
    },

    "Programming": {
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
    },

    "Web Development": {
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue.js",
        "Node.js",
        "Django",
        "Flask",
        "FastAPI",
        "REST API",
    },

    "Databases": {
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Oracle Database",
        "Redis",
    },

    "Cloud": {
        "AWS",
        "Microsoft Azure",
        "Google Cloud",
    },

    "DevOps": {
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub",
        "Jenkins",
        "CI/CD",
    },

    "Core CS": {
        "Data Structures",
        "Algorithms",
        "Object-Oriented Programming",
        "DBMS",
        "Operating Systems",
        "Computer Networks",
    },

    "Business / Soft Skills": {
        "PowerPoint",
        "Communication",
        "Problem Solving",
    },
}


# ============================================================
# BUILD REVERSE LOOKUP
# ============================================================

SKILL_TO_CATEGORY = {}

for category, skills in SKILL_CATEGORIES.items():

    for skill in skills:

        SKILL_TO_CATEGORY[skill] = category


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize job-posting text before skill matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Normalize unicode-style dashes
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize common separators
    text = text.replace("_", " ")
    text = text.replace("-", " ")

    # Normalize slash spacing
    text = re.sub(
        r"\s*/\s*",
        "/",
        text
    )

    # Normalize plus signs
    text = re.sub(
        r"\s*\+\s*",
        "+",
        text
    )

    # Collapse whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CREATE SAFE REGEX PATTERN
# ============================================================

def build_skill_pattern(
    variation: str
) -> str:
    """
    Build a regex pattern that matches a skill
    as a complete word or phrase.
    """

    variation = normalize_text(
        variation
    )

    escaped = re.escape(
        variation
    )

    # Word-like boundary.
    #
    # This prevents:
    #
    # java
    #
    # from matching:
    #
    # javascript
    #
    # and prevents:
    #
    # react
    #
    # from matching unrelated words.
    pattern = (
        r"(?<![a-z0-9])"
        + escaped
        + r"(?![a-z0-9])"
    )

    return pattern


# ============================================================
# SKILL MATCHING
# ============================================================

def skill_exists(
    text: str,
    variation: str
) -> bool:
    """
    Check whether a skill variation exists
    as a meaningful word/phrase in the text.
    """

    normalized_text = normalize_text(
        text
    )

    normalized_variation = normalize_text(
        variation
    )

    if not normalized_text:
        return False

    if not normalized_variation:
        return False

    pattern = build_skill_pattern(
        normalized_variation
    )

    return (
        re.search(
            pattern,
            normalized_text
        )
        is not None
    )


# ============================================================
# FIND SKILL EVIDENCE
# ============================================================

def find_skill_evidence(
    text: str,
    variation: str
) -> str:
    """
    Return the actual matched skill variation.

    This is useful for research because we can later
    store evidence showing why a skill was detected.
    """

    normalized_text = normalize_text(
        text
    )

    normalized_variation = normalize_text(
        variation
    )

    if not normalized_text:
        return ""

    pattern = build_skill_pattern(
        normalized_variation
    )

    match = re.search(
        pattern,
        normalized_text
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(
    text: str
) -> list[str]:
    """
    Extract standardized skills from job-posting text.
    """

    normalized_text = normalize_text(
        text
    )

    if not normalized_text:
        return []

    found_skills = []

    for standard_skill, variations in SKILL_TAXONOMY.items():

        # Check longer phrases first.
        #
        # Example:
        #
        # "machine learning"
        #
        # should be checked before
        #
        # "ml"
        #
        sorted_variations = sorted(
            variations,
            key=len,
            reverse=True
        )

        for variation in sorted_variations:

            if skill_exists(
                normalized_text,
                variation
            ):

                found_skills.append(
                    standard_skill
                )

                break

    return found_skills


# ============================================================
# EXTRACT SKILL EVIDENCE
# ============================================================

def extract_skill_evidence(
    text: str
) -> dict:
    """
    Extract standardized skills together with
    the variation that triggered the detection.

    Example:

    {
        "SQL": "sql",
        "Power BI": "power bi",
        "Python": "python"
    }
    """

    normalized_text = normalize_text(
        text
    )

    evidence = {}

    if not normalized_text:
        return evidence

    for standard_skill, variations in SKILL_TAXONOMY.items():

        sorted_variations = sorted(
            variations,
            key=len,
            reverse=True
        )

        for variation in sorted_variations:

            matched_text = find_skill_evidence(
                normalized_text,
                variation
            )

            if matched_text:

                evidence[
                    standard_skill
                ] = matched_text

                break

    return evidence


# ============================================================
# EXTRACT SKILL CATEGORIES
# ============================================================

def get_skill_categories(
    skills: list[str]
) -> list[str]:
    """
    Convert detected skills into their
    standardized categories.
    """

    categories = set()

    for skill in skills:

        category = SKILL_TO_CATEGORY.get(
            skill
        )

        if category:
            categories.add(
                category
            )

    return sorted(
        categories
    )


# ============================================================
# EXTRACT SKILLS FROM JOB
# ============================================================

def extract_job_skills(
    job: dict
) -> dict:
    """
    Extract skills from both the job title
    and job description.
    """

    title = job.get(
        "title",
        ""
    )

    description = job.get(
        "description",
        ""
    )

    combined_text = (
        f"{title} {description}"
    )

    skills = extract_skills(
        combined_text
    )

    evidence = extract_skill_evidence(
        combined_text
    )

    categories = get_skill_categories(
        skills
    )

    return {
        **job,

        "skills": skills,

        "skill_count": len(
            skills
        ),

        "skill_evidence": evidence,

        "skill_categories": categories,
    }


# ============================================================
# PROCESS MULTIPLE JOBS
# ============================================================

def extract_skills_from_jobs(
    jobs: list[dict]
) -> list[dict]:
    """
    Extract skills from every processed job.
    """

    processed_jobs = []

    for job in jobs:

        processed_job = extract_job_skills(
            job
        )

        processed_jobs.append(
            processed_job
        )

    return processed_jobs


# ============================================================
# SKILL DEMAND ANALYSIS
# ============================================================

def calculate_skill_demand(
    jobs: list[dict]
) -> list[dict]:
    """
    Calculate how frequently each skill appears
    across job postings.

    Demand % =
        jobs containing skill /
        total jobs
        × 100
    """

    total_jobs = len(
        jobs
    )

    if total_jobs == 0:
        return []

    skill_job_counts = defaultdict(
        int
    )

    for job in jobs:

        # One job contributes only once
        # to a skill's demand.
        unique_skills = set(
            job.get(
                "skills",
                []
            )
        )

        for skill in unique_skills:

            skill_job_counts[
                skill
            ] += 1

    demand_results = []

    for skill, job_count in (
        skill_job_counts.items()
    ):

        demand_percentage = (
            job_count /
            total_jobs
        ) * 100

        category = (
            SKILL_TO_CATEGORY.get(
                skill,
                "Other"
            )
        )

        demand_results.append(
            {
                "skill": skill,

                "category": category,

                "job_count": job_count,

                "total_jobs": total_jobs,

                "demand_percentage": round(
                    demand_percentage,
                    2
                ),
            }
        )

    # Highest demand first
    demand_results.sort(
        key=lambda item: (
            item["demand_percentage"],
            item["skill"]
        ),
        reverse=True
    )

    return demand_results


# ============================================================
# ROLE-WISE SKILL DEMAND
# ============================================================

def calculate_role_skill_demand(
    jobs: list[dict],
    role: str
) -> list[dict]:
    """
    Calculate skill demand for one normalized role.
    """

    role_jobs = [

        job

        for job in jobs

        if job.get(
            "normalized_role"
        ) == role
    ]

    return calculate_skill_demand(
        role_jobs
    )