from market_engine.models import JobPosting
from market_engine.processor import (
    process_jobs,
    summarize_jobs
)


jobs = [

    JobPosting(
        source="adzuna",
        source_job_id="1001",
        title="Senior Data Analyst",
        company="ABC Technologies Pvt Ltd",
        location="Puducherry",
        description="""
        We are looking for a Data Analyst with
        strong SQL, Python, Excel and Power BI skills.
        """,
        url="https://example.com/job1",
        query="data analyst"
    ),

    JobPosting(
        source="adzuna",
        source_job_id="1002",
        title="BI Analyst",
        company="ABC Technologies Pvt Ltd",
        location="Puducherry",
        description="""
        We are looking for a BI Analyst with
        strong SQL, Python, Excel and Power BI skills.
        """,
        url="https://example.com/job2",
        query="data analyst"
    ),

    JobPosting(
        source="adzuna",
        source_job_id="1003",
        title="Python Developer",
        company="XYZ Software",
        location="Chennai",
        description="""
        Python developer required with Django,
        REST API and PostgreSQL experience.
        """,
        url="https://example.com/job3",
        query="python developer"
    ),
]


processed_jobs = process_jobs(jobs)


print("\n========================================")
print("SKILLFORAGE MARKET ENGINE")
print("========================================")

print("\nProcessed Jobs:")

for job in processed_jobs:

    print("\n----------------------------------------")

    print("Job ID:",
          job["source_job_id"])

    print("Original Title:",
          job["title"])

    print("Normalized Role:",
          job["normalized_role"])

    print("Company:",
          job["company"])

    print("Location:",
          job["location"])


print("\n========================================")
print("DATASET SUMMARY")
print("========================================")

summary = summarize_jobs(processed_jobs)

print("Total Jobs:",
      summary["total_jobs"])

print("Role Distribution:")

for role, count in summary["role_distribution"].items():

    print(
        f"  {role}: {count}"
    )