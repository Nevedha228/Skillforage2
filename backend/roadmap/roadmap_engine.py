import re


# ============================================================
# SKILL INFORMATION
# ============================================================
#
# Each skill has:
#
# category
# priority
# estimated learning weeks
#
# Priority:
# 5 = very important
# 4 = important
# 3 = moderate
# 2 = supporting
# 1 = optional
#
# ============================================================

SKILL_INFO = {

    # --------------------------------------------------------
    # Programming
    # --------------------------------------------------------

    "python": {
        "category": "Programming",
        "priority": 5,
        "weeks": 3
    },

    "java": {
        "category": "Programming",
        "priority": 5,
        "weeks": 3
    },

    "javascript": {
        "category": "Programming",
        "priority": 4,
        "weeks": 3
    },

    # --------------------------------------------------------
    # DSA / Core CS
    # --------------------------------------------------------

    "data structures": {
        "category": "DSA",
        "priority": 5,
        "weeks": 4
    },

    "object oriented programming": {
        "category": "Core CS",
        "priority": 5,
        "weeks": 2
    },

    "dbms": {
        "category": "Core CS",
        "priority": 5,
        "weeks": 2
    },

    "operating systems": {
        "category": "Core CS",
        "priority": 4,
        "weeks": 2
    },

    "computer networks": {
        "category": "Core CS",
        "priority": 4,
        "weeks": 2
    },

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    "sql": {
        "category": "Database",
        "priority": 5,
        "weeks": 3
    },

    "mysql": {
        "category": "Database",
        "priority": 4,
        "weeks": 2
    },

    "mongodb": {
        "category": "Database",
        "priority": 3,
        "weeks": 2
    },

    # --------------------------------------------------------
    # Web Development
    # --------------------------------------------------------

    "html": {
        "category": "Web Development",
        "priority": 3,
        "weeks": 1
    },

    "css": {
        "category": "Web Development",
        "priority": 3,
        "weeks": 1
    },

    "react": {
        "category": "Web Development",
        "priority": 4,
        "weeks": 3
    },

    "node": {
        "category": "Backend Development",
        "priority": 4,
        "weeks": 3
    },

    "spring boot": {
        "category": "Backend Development",
        "priority": 4,
        "weeks": 3
    },

    "rest api": {
        "category": "Backend Development",
        "priority": 4,
        "weeks": 2
    },

    # --------------------------------------------------------
    # Tools
    # --------------------------------------------------------

    "git": {
        "category": "Tools",
        "priority": 4,
        "weeks": 1
    },

    "github": {
        "category": "Tools",
        "priority": 3,
        "weeks": 1
    },

    # --------------------------------------------------------
    # AI / Data
    # --------------------------------------------------------

    "machine learning": {
        "category": "AI & Data",
        "priority": 5,
        "weeks": 4
    },

    "deep learning": {
        "category": "AI & Data",
        "priority": 4,
        "weeks": 4
    },

    "data science": {
        "category": "AI & Data",
        "priority": 5,
        "weeks": 4
    },

    "pandas": {
        "category": "AI & Data",
        "priority": 4,
        "weeks": 2
    },

    "numpy": {
        "category": "AI & Data",
        "priority": 4,
        "weeks": 2
    },

    # --------------------------------------------------------
    # Default / Unknown
    # --------------------------------------------------------

    "default": {
        "category": "Technical Skill",
        "priority": 3,
        "weeks": 2
    }
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(skill):

    skill = str(skill).lower().strip()

    skill = re.sub(
        r"^[•\-*]\s*",
        "",
        skill
    )

    skill = skill.replace(
        "javascript",
        "javascript"
    )

    skill = skill.replace(
        "react.js",
        "react"
    )

    skill = skill.replace(
        "reactjs",
        "react"
    )

    skill = skill.replace(
        "node.js",
        "node"
    )

    skill = skill.replace(
        "nodejs",
        "node"
    )

    skill = skill.replace(
        "springboot",
        "spring boot"
    )

    skill = skill.replace(
        "restapi",
        "rest api"
    )

    skill = skill.replace(
        "oops",
        "object oriented programming"
    )

    skill = skill.strip()

    return skill


# ============================================================
# TIME MANAGEMENT
# ============================================================

def get_weekly_capacity(time_available):

    value = str(
        time_available
    ).lower().strip()

    if not value:
        return 7

    # --------------------------------------------------------
    # Look for numbers
    # --------------------------------------------------------

    numbers = re.findall(
        r"\d+",
        value
    )

    if numbers:

        hours = int(
            numbers[0]
        )

        # If user says 10 hours/week etc.
        if "week" in value:

            return max(
                hours,
                3
            )

        # If user says 2 hours/day
        if "day" in value:

            return max(
                hours * 7,
                3
            )

    # --------------------------------------------------------
    # Common text options
    # --------------------------------------------------------

    if "low" in value:
        return 5

    if "medium" in value:
        return 10

    if "high" in value:
        return 15

    if "1 hour" in value:
        return 7

    if "2 hour" in value:
        return 14

    if "3 hour" in value:
        return 21

    return 7


# ============================================================
# YEAR TYPE
# ============================================================

def classify_student_year(year):

    value = str(
        year
    ).lower().strip()

    if "1" in value:
        return "early"

    if "2" in value:
        return "developing"

    if "3" in value:
        return "placement_prep"

    if "4" in value:
        return "final_year"

    if "final" in value:
        return "final_year"

    return "developing"


# ============================================================
# TARGET ROLE MATCHING
# ============================================================

def role_bonus(skill, target_role):

    role = str(
        target_role
    ).lower()

    skill = normalize_skill(
        skill
    )

    bonus = 0

    # --------------------------------------------------------
    # Data Scientist
    # --------------------------------------------------------

    if (
        "data scientist" in role
        or "data science" in role
    ):

        if skill in [
            "python",
            "sql",
            "data science",
            "machine learning",
            "pandas",
            "numpy"
        ]:

            bonus = 3

    # --------------------------------------------------------
    # Software Developer
    # --------------------------------------------------------

    elif (
        "software" in role
        or "developer" in role
        or "software engineer" in role
    ):

        if skill in [
            "java",
            "python",
            "data structures",
            "object oriented programming",
            "sql",
            "git"
        ]:

            bonus = 3

    # --------------------------------------------------------
    # Full Stack
    # --------------------------------------------------------

    elif "full stack" in role:

        if skill in [
            "html",
            "css",
            "javascript",
            "react",
            "node",
            "sql",
            "rest api"
        ]:

            bonus = 3

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    elif (
        "ai" in role
        or "machine learning" in role
    ):

        if skill in [
            "python",
            "machine learning",
            "deep learning",
            "numpy",
            "pandas",
            "data science"
        ]:

            bonus = 3

    return bonus


# ============================================================
# INTEREST MATCHING
# ============================================================

def interest_bonus(skill, interests):

    skill = normalize_skill(
        skill
    )

    if not interests:
        return 0

    if isinstance(
        interests,
        str
    ):

        interests_text = interests.lower()

    else:

        interests_text = " ".join(
            str(item).lower()
            for item in interests
        )

    bonus = 0

    if (
        "data" in interests_text
        or "analytics" in interests_text
    ):

        if skill in [
            "python",
            "sql",
            "data science",
            "machine learning",
            "pandas",
            "numpy"
        ]:

            bonus += 2

    if (
        "ai" in interests_text
        or "artificial intelligence" in interests_text
    ):

        if skill in [
            "python",
            "machine learning",
            "deep learning",
            "data science"
        ]:

            bonus += 2

    if (
        "web" in interests_text
        or "development" in interests_text
    ):

        if skill in [
            "html",
            "css",
            "javascript",
            "react",
            "node",
            "spring boot",
            "rest api"
        ]:

            bonus += 2

    if "java" in interests_text:

        if skill in [
            "java",
            "object oriented programming",
            "data structures",
            "spring boot"
        ]:

            bonus += 2

    return bonus


# ============================================================
# LEARNING FOCUS
# ============================================================

def get_learning_focus(
    skill,
    category
):

    skill = normalize_skill(
        skill
    )

    focus_map = {

        "python": [
            "Syntax and core programming",
            "Functions and modules",
            "OOP",
            "File handling",
            "Problem solving"
        ],

        "java": [
            "Core Java",
            "OOP",
            "Collections",
            "Exception handling",
            "Problem solving"
        ],

        "sql": [
            "SELECT queries",
            "Filtering and sorting",
            "JOINs",
            "GROUP BY",
            "Subqueries",
            "Window functions"
        ],

        "data structures": [
            "Arrays",
            "Strings",
            "Hashing",
            "Stacks and queues",
            "Linked lists",
            "Trees",
            "Searching and sorting"
        ],

        "object oriented programming": [
            "Classes and objects",
            "Inheritance",
            "Polymorphism",
            "Abstraction",
            "Encapsulation"
        ],

        "machine learning": [
            "Data preprocessing",
            "Regression",
            "Classification",
            "Model evaluation",
            "Feature engineering"
        ],

        "data science": [
            "Python for data",
            "Data cleaning",
            "Exploratory data analysis",
            "Visualization",
            "Statistics",
            "Machine learning basics"
        ],

        "pandas": [
            "Series and DataFrames",
            "Data cleaning",
            "Filtering",
            "Grouping",
            "Merging datasets"
        ],

        "numpy": [
            "Arrays",
            "Indexing",
            "Vectorized operations",
            "Statistics",
            "Linear algebra basics"
        ],

        "react": [
            "Components",
            "Props",
            "State",
            "Hooks",
            "API integration"
        ],

        "html": [
            "Semantic HTML",
            "Forms",
            "Tables",
            "Accessibility basics"
        ],

        "css": [
            "Selectors",
            "Flexbox",
            "Grid",
            "Responsive design"
        ],

        "git": [
            "Repositories",
            "Commits",
            "Branches",
            "Merge",
            "Pull requests"
        ]
    }

    return focus_map.get(
        skill,
        [
            f"{skill.title()} fundamentals",
            f"Practical {skill.title()} usage",
            f"Build a small project using {skill.title()}",
            f"Practice interview questions"
        ]
    )


# ============================================================
# PROJECT SUGGESTION
# ============================================================

def project_for_skill(skill):

    skill = normalize_skill(
        skill
    )

    projects = {

        "python":
            "Build a Python automation or data-analysis project.",

        "java":
            "Build a Java application using OOP and collections.",

        "sql":
            "Build a database project with complex SQL queries.",

        "data structures":
            "Build a DSA problem-solving tracker.",

        "machine learning":
            "Build an end-to-end machine learning prediction project.",

        "data science":
            "Build a complete data-analysis project using a real dataset.",

        "pandas":
            "Perform EDA on a real-world dataset using Pandas.",

        "numpy":
            "Create a numerical data-processing mini project.",

        "react":
            "Build an interactive React dashboard.",

        "html":
            "Build a responsive portfolio webpage.",

        "css":
            "Create a responsive UI component collection.",

        "git":
            "Create and manage a project using Git branches and pull requests."
    }

    return projects.get(
        skill,
        f"Build a small practical project using {skill.title()}."
    )


# ============================================================
# MAIN ROADMAP ENGINE
# ============================================================

def generate_roadmap(
    missing_skills,
    matched_skills=None,
    education="",
    year="",
    branch="",
    career_status="",
    interests=None,
    time_available="",
    target_role=""
):

    if matched_skills is None:
        matched_skills = []

    if interests is None:
        interests = []

    # --------------------------------------------------------
    # Clean skills
    # --------------------------------------------------------

    cleaned_missing = []

    for skill in missing_skills:

        if not skill:
            continue

        skill = normalize_skill(
            skill
        )

        if skill and skill not in cleaned_missing:

            cleaned_missing.append(
                skill
            )

    # --------------------------------------------------------
    # Determine student stage
    # --------------------------------------------------------

    student_stage = classify_student_year(
        year
    )

    weekly_hours = get_weekly_capacity(
        time_available
    )

    # --------------------------------------------------------
    # Score every missing skill
    # --------------------------------------------------------

    scored_skills = []

    for skill in cleaned_missing:

        info = SKILL_INFO.get(
            skill,
            SKILL_INFO["default"]
        )

        score = (
            info["priority"]
            + role_bonus(
                skill,
                target_role
            )
            + interest_bonus(
                skill,
                interests
            )
        )

        scored_skills.append({

            "skill": skill,

            "category": info["category"],

            "priority_score": score,

            "base_priority": info["priority"],

            "estimated_weeks": info["weeks"]

        })

    # --------------------------------------------------------
    # Sort highest priority first
    # --------------------------------------------------------

    scored_skills.sort(
        key=lambda item: (
            -item["priority_score"],
            item["estimated_weeks"]
        )
    )

    # --------------------------------------------------------
    # Number of roadmap skills
    # --------------------------------------------------------
    #
    # Final-year students:
    # Focus only on the most important skills.
    #
    # Early-year students:
    # Build a broader foundation.
    #
    # --------------------------------------------------------

    if student_stage == "final_year":

        max_skills = 5

    elif student_stage == "placement_prep":

        max_skills = 6

    elif student_stage == "early":

        max_skills = 10

    else:

        max_skills = 8

    selected_skills = scored_skills[
        :max_skills
    ]

    # --------------------------------------------------------
    # Create roadmap phases
    # --------------------------------------------------------

    phases = []

    for index, item in enumerate(
        selected_skills,
        start=1
    ):

        skill = item["skill"]

        focus = get_learning_focus(
            skill,
            item["category"]
        )

        project = project_for_skill(
            skill
        )

        # ----------------------------------------------------
        # Phase duration
        # ----------------------------------------------------

        estimated_weeks = item[
            "estimated_weeks"
        ]

        # More weekly hours = faster roadmap
        if weekly_hours >= 15:

            duration = max(
                1,
                round(
                    estimated_weeks * 0.65
                )
            )

        elif weekly_hours >= 10:

            duration = max(
                1,
                round(
                    estimated_weeks * 0.8
                )
            )

        elif weekly_hours <= 5:

            duration = round(
                estimated_weeks * 1.4
            )

        else:

            duration = estimated_weeks

        phases.append({

            "phase": index,

            "skill": skill.title(),

            "category": item[
                "category"
            ],

            "priority": (
                "High"
                if item["priority_score"] >= 7
                else "Medium"
            ),

            "duration_weeks": duration,

            "focus": focus,

            "project": project,

            "status": "Not Started"

        })

    # --------------------------------------------------------
    # Calculate total duration
    # --------------------------------------------------------

    total_weeks = sum(
        phase["duration_weeks"]
        for phase in phases
    )

    # --------------------------------------------------------
    # Personalized roadmap type
    # --------------------------------------------------------

    if student_stage == "final_year":

        roadmap_type = (
            "Placement-Focused Smart Roadmap"
        )

    elif student_stage == "placement_prep":

        roadmap_type = (
            "Career Preparation Roadmap"
        )

    elif student_stage == "early":

        roadmap_type = (
            "Foundation & Skill Mastery Roadmap"
        )

    else:

        roadmap_type = (
            "Skill Development Roadmap"
        )

    # --------------------------------------------------------
    # Generate weekly recommendation
    # --------------------------------------------------------

    if weekly_hours <= 5:

        weekly_plan = (
            "Focus on one skill at a time "
            "with short daily practice sessions."
        )

    elif weekly_hours <= 10:

        weekly_plan = (
            "Divide your time between learning, "
            "practice and project work."
        )

    else:

        weekly_plan = (
            "Use a balanced schedule with learning, "
            "coding practice, projects and revision."
        )

    # --------------------------------------------------------
    # Return complete roadmap
    # --------------------------------------------------------

    return {

        "success": True,

        "roadmap_type": roadmap_type,

        "student_profile": {

            "education": education,

            "year": year,

            "branch": branch,

            "career_status": career_status,

            "target_role": target_role,

            "interests": interests,

            "weekly_hours": weekly_hours

        },

        "roadmap_summary": {

            "skills_to_learn": len(
                phases
            ),

            "estimated_duration_weeks": total_weeks,

            "weekly_plan": weekly_plan

        },

        "priority_skills": [
            item["skill"]
            for item in selected_skills
        ],

        "phases": phases

    }