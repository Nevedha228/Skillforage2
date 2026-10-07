from market_engine.analytics import (
    get_top_skills,
    get_role_distribution,
    get_role_skill_analysis,
    get_salary_analysis,
    get_location_distribution,
)


# ============================================================
# SKILLFORAGE MARKET ANALYTICS TEST
# ============================================================

print("\n")
print("=" * 60)
print("SKILLFORAGE MARKET ANALYTICS")
print("=" * 60)


# ============================================================
# TOP SKILLS
# ============================================================

print("\n")
print("=" * 60)
print("TOP MARKET SKILLS")
print("=" * 60)

top_skills = get_top_skills(
    limit=10
)

for item in top_skills:

    print(
        f'{item["skill"]}: '
        f'{item["job_count"]}/'
        f'{item["total_jobs"]} jobs '
        f'({item["demand_percentage"]}%)'
    )


# ============================================================
# ROLE DISTRIBUTION
# ============================================================

print("\n")
print("=" * 60)
print("ROLE DISTRIBUTION")
print("=" * 60)

roles = get_role_distribution()

for item in roles:

    print(
        f'{item["role"]}: '
        f'{item["job_count"]} jobs'
    )


# ============================================================
# DATA ANALYST SKILLS
# ============================================================

print("\n")
print("=" * 60)
print("DATA ANALYST SKILL DEMAND")
print("=" * 60)

data_analyst_skills = (
    get_role_skill_analysis(
        role="Data Analyst",
        limit=10
    )
)

for item in data_analyst_skills:

    print(
        f'{item["skill"]}: '
        f'{item["job_count"]}/'
        f'{item["total_jobs"]} jobs '
        f'({item["demand_percentage"]}%)'
    )


# ============================================================
# SALARY
# ============================================================

print("\n")
print("=" * 60)
print("SALARY ANALYSIS")
print("=" * 60)

salary = get_salary_analysis(
    normalized_role="Data Analyst"
)

print(
    "Jobs with salary:",
    salary["jobs_with_salary"]
)

print(
    "Average minimum salary:",
    salary["average_min_salary"]
)

print(
    "Average maximum salary:",
    salary["average_max_salary"]
)

print(
    "Minimum salary:",
    salary["minimum_salary"]
)

print(
    "Maximum salary:",
    salary["maximum_salary"]
)


# ============================================================
# LOCATIONS
# ============================================================

print("\n")
print("=" * 60)
print("TOP JOB LOCATIONS")
print("=" * 60)

locations = get_location_distribution(
    limit=10
)

for item in locations:

    print(
        f'{item["location"]}: '
        f'{item["job_count"]} jobs'
    )


print("\n")
print("=" * 60)
print("ANALYTICS TEST COMPLETED")
print("=" * 60)