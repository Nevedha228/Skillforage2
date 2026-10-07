from market_engine.skill_extractor import (
    extract_skills,
    calculate_skill_demand
)


# ============================================================
# TEST JOB DATA
# ============================================================

jobs = [

    {
        "title": "Data Analyst",
        "description": """
        We are looking for a Data Analyst with
        strong SQL, Python, Excel and Power BI skills.
        Experience with Tableau and statistics is preferred.
        """
    },

    {
        "title": "Business Intelligence Analyst",
        "description": """
        Candidate should have experience with
        Power BI, SQL, Excel and Python.
        Strong data visualization skills are required.
        """
    },

    {
        "title": "Junior Data Analyst",
        "description": """
        Knowledge of SQL, Excel and Power BI is required.
        Python and statistics will be an advantage.
        """
    }
]


# ============================================================
# EXTRACT SKILLS
# ============================================================

print("\n========================================")
print("SKILLFORAGE SKILL EXTRACTION")
print("========================================")


for index, job in enumerate(
    jobs,
    start=1
):

    text = (
        job["title"]
        + " "
        + job["description"]
    )

    skills = extract_skills(text)

    job["skills"] = skills

    print(
        f"\nJob {index}:"
    )

    print(
        "Title:",
        job["title"]
    )

    print(
        "Skills:",
        ", ".join(skills)
    )


# ============================================================
# DEMAND ANALYSIS
# ============================================================

print("\n========================================")
print("SKILL DEMAND")
print("========================================")


demand = calculate_skill_demand(
    jobs
)


for item in demand:

    print(
        f'{item["skill"]}: '
        f'{item["job_count"]}/'
        f'{item["total_jobs"]} jobs '
        f'({item["demand_percentage"]}%)'
    )