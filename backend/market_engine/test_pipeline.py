from market_engine.pipeline import run_market_pipeline

from market_engine.database import (
    get_database_statistics,
)


# ============================================================
# MARKET PIPELINE TEST
# ============================================================

ROLE = "data analyst"

# IMPORTANT:
# Keep the SAME Adzuna country code
# that already worked in your previous test.

COUNTRY = "in"

LOCATION = ""


print("\n")
print("=" * 50)
print("SKILLFORAGE MARKET INTELLIGENCE")
print("=" * 50)

print(
    "\nSearching for:",
    ROLE
)


try:

    result = run_market_pipeline(

        role=ROLE,

        country=COUNTRY,

        pages=1,

        results_per_page=20,

        location=LOCATION,
    )

    # ========================================================
    # COLLECTION RESULT
    # ========================================================

    print("\n")
    print("=" * 50)
    print("COLLECTION RESULT")
    print("=" * 50)

    print(
        "Raw jobs:",
        result[
            "raw_job_count"
        ]
    )

    print(
        "Processed jobs:",
        result[
            "processed_job_count"
        ]
    )

    # ========================================================
    # TOP MARKET SKILLS
    # ========================================================

    print("\n")
    print("=" * 50)
    print("TOP MARKET SKILLS")
    print("=" * 50)

    for item in result[
        "skill_demand"
    ][:15]:

        print(
            f'{item["skill"]}: '
            f'{item["job_count"]}/'
            f'{item["total_jobs"]} jobs '
            f'({item["demand_percentage"]}%)'
        )

    # ========================================================
    # NORMALIZED ROLES
    # ========================================================

    print("\n")
    print("=" * 50)
    print("NORMALIZED ROLES")
    print("=" * 50)

    for (
        role_name,
        skills
    ) in result[
        "role_skill_demand"
    ].items():

        print(
            f"\n{role_name}"
        )

        for item in skills[:5]:

            print(
                f'  {item["skill"]}: '
                f'{item["demand_percentage"]}%'
            )

    # ========================================================
    # DATABASE STATISTICS
    # ========================================================

    statistics = (
        get_database_statistics()
    )

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
    print("MARKET PIPELINE COMPLETED")
    print("=" * 50)


except Exception as error:

    print("\n")
    print("❌ MARKET PIPELINE ERROR")

    print(
        type(error).__name__,
        ":",
        error
    )