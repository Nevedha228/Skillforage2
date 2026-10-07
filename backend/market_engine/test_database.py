from market_engine.database import (
    initialize_database,
    get_database_statistics,
    save_job,
)


# ============================================================
# DATABASE TEST
# ============================================================

print("\n")
print("=" * 50)
print("SKILLFORAGE MARKET DATABASE TEST")
print("=" * 50)


# ============================================================
# STEP 1 — CREATE TABLES
# ============================================================

print("\nCreating database...")

initialize_database()

print("Database initialized successfully.")


# ============================================================
# STEP 2 — TEST JOB
# ============================================================

test_job = {

    "source": "test",

    "source_job_id": "TEST_JOB_001",

    "title": "Data Analyst",

    "normalized_role": "Data Analyst",

    "company": "SkillForage Test Company",

    "location": "Puducherry",

    "description": (
        "Data Analyst with SQL, Python, "
        "Excel and Power BI experience."
    ),

    "url": "https://example.com/job",

    "category": "Data Analytics",

    "salary_min": None,

    "salary_max": None,

    "contract_type": "",

    "contract_time": "",

    "created_at": "",

    "collected_at": "2026-10-05T00:00:00+00:00",

    "query": "data analyst",

    "page": 1,

    "skills": [
        "SQL",
        "Python",
        "Excel",
        "Power BI",
    ],

    "skill_evidence": {
        "SQL": "sql",
        "Python": "python",
        "Excel": "excel",
        "Power BI": "power bi",
    },
}


# ============================================================
# STEP 3 — SAVE JOB
# ============================================================

print("\nSaving test job...")

job_id = save_job(
    test_job
)

print(
    "Saved database job ID:",
    job_id
)


# ============================================================
# STEP 4 — SHOW STATISTICS
# ============================================================

statistics = get_database_statistics()

print("\n")
print("=" * 50)
print("DATABASE STATISTICS")
print("=" * 50)

print(
    "Jobs:",
    statistics["jobs"]
)

print(
    "Skills:",
    statistics["skills"]
)

print(
    "Job-Skill relationships:",
    statistics["job_skills"]
)

print(
    "Market snapshots:",
    statistics["market_snapshots"]
)

print("\n")
print("=" * 50)
print("DATABASE TEST COMPLETED")
print("=" * 50)