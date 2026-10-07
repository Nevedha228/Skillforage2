import re


# ============================================================
# SKILL INFORMATION
# ============================================================

SKILL_INFO = {

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

    skill = str(
        skill
    ).lower().strip()

    skill = re.sub(
        r"^[•\-*]\s*",
        "",
        skill
    )

    skill = skill.replace(
        "-",
        " "
    )

    skill = skill.replace(
        "_",
        " "
    )

    skill = skill.replace(
        ".",
        ""
    )

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    aliases = {

        "reactjs": "react",
        "react js": "react",

        "nodejs": "node",
        "node js": "node",

        "dsa": "data structures",
        "data structures and algorithms": "data structures",

        "oops": "object oriented programming",
        "oop": "object oriented programming",

        "springboot": "spring boot",

        "restapi": "rest api",

        "js": "javascript",

        "py": "python"
    }

    return aliases.get(
        skill,
        skill
    )


# ============================================================
# WEEKLY CAPACITY
# ============================================================

def get_weekly_capacity(
    time_available
):

    value = str(
        time_available
    ).lower().strip()

    if not value:
        return 7

    numbers = re.findall(
        r"\d+",
        value
    )

    if numbers:

        hours = int(
            numbers[0]
        )

        if "week" in value:

            return max(
                hours,
                3
            )

        if "day" in value:

            return max(
                hours * 7,
                3
            )

    if "low" in value:
        return 5

    if "medium" in value:
        return 10

    if "high" in value:
        return 15

    return 7


# ============================================================
# STUDENT YEAR
# ============================================================

def classify_student_year(year):

    value = str(
        year
    ).lower().strip()

    if (
        "final" in value
        or "4th" in value
        or "4 year" in value
        or "fourth" in value
    ):
        return "final_year"

    if (
        "3rd" in value
        or "3 year" in value
        or "third" in value
    ):
        return "placement_prep"

    if (
        "2nd" in value
        or "2 year" in value
        or "second" in value
    ):
        return "developing"

    if (
        "1st" in value
        or "1 year" in value
        or "first" in value
    ):
        return "early"

    return "developing"


# ============================================================
# ROLE BONUS
# ============================================================

def role_bonus(
    skill,
    target_role
):

    role = str(
        target_role
    ).lower()

    skill = normalize_skill(
        skill
    )

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
            return 3

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
            return 3

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
            return 3

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
            return 3

    return 0


# ============================================================
# INTEREST BONUS
# ============================================================

def interest_bonus(
    skill,
    interests
):

    skill = normalize_skill(
        skill
    )

    if not interests:
        return 0

    if isinstance(
        interests,
        str
    ):

        text = interests.lower()

    else:

        text = " ".join(
            str(item).lower()
            for item in interests
        )

    bonus = 0

    if (
        "data" in text
        or "analytics" in text
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
        "ai" in text
        or "artificial intelligence" in text
    ):

        if skill in [
            "python",
            "machine learning",
            "deep learning",
            "data science"
        ]:
            bonus += 2

    if (
        "web" in text
        or "development" in text
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

    if "java" in text:

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

def get_learning_focus(skill):

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
            "Practice interview questions"
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
            "Create a numerical data-processing project.",

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

    if missing_skills is None:
        missing_skills = []

    if matched_skills is None:
        matched_skills = []

    if interests is None:
        interests = []

    if not isinstance(
        missing_skills,
        list
    ):
        missing_skills = [
            missing_skills
        ]

    student_stage = classify_student_year(
        year
    )

    weekly_hours = get_weekly_capacity(
        time_available
    )

    cleaned_missing = []

    for skill in missing_skills:

        normalized = normalize_skill(
            skill
        )

        if (
            normalized
            and normalized not in cleaned_missing
        ):

            cleaned_missing.append(
                normalized
            )

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

    scored_skills.sort(
        key=lambda item: (
            -item["priority_score"],
            item["estimated_weeks"]
        )
    )

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

    phases = []

    for index, item in enumerate(
        selected_skills,
        start=1
    ):

        skill = item["skill"]

        estimated_weeks = item[
            "estimated_weeks"
        ]

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

            duration = max(
                1,
                round(
                    estimated_weeks * 1.4
                )
            )

        else:

            duration = estimated_weeks

        phases.append({

            "phase": index,

            "skill": skill.title(),

            "category": item["category"],

            "priority": (
                "High"
                if item["priority_score"] >= 7
                else "Medium"
            ),

            "priority_score": item[
                "priority_score"
            ],

            "duration_weeks": duration,

            "focus": get_learning_focus(
                skill
            ),

            "project": project_for_skill(
                skill
            ),

            "status": "Not Started"

        })

    total_weeks = sum(
        phase["duration_weeks"]
        for phase in phases
    )

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


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    result = generate_roadmap(

        missing_skills=[
            "Python",
            "SQL",
            "Data Structures",
            "Machine Learning"
        ],

        matched_skills=[
            "Java"
        ],

        education="engineering",

        year="4th Year",

        branch="cse",

        career_status="student",

        interests=[
            "Data Science",
            "AI"
        ],

        time_available="10 hours/week",

        target_role="Data Scientist"
    )

    print(result)