import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

from .models import JobPosting


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"


# ============================================================
# FETCH JOBS FROM ADZUNA
# ============================================================

def fetch_adzuna_jobs(
    role: str,
    country: str,
    pages: int = 3,
    results_per_page: int = 20,
    location: str = "",
):
    """
    Collect job postings from Adzuna.

    This function is designed for the SkillForage
    Labor Market Intelligence Engine.

    Parameters
    ----------
    role : str
        Target role, e.g. "Data Analyst"

    country : str
        Adzuna country code configured for the project.

    pages : int
        Number of result pages to collect.

    results_per_page : int
        Number of jobs requested per page.

    location : str
        Optional location filter.

    Returns
    -------
    list[JobPosting]
        Standardized job postings.
    """

    # ========================================================
    # CHECK API CREDENTIALS
    # ========================================================

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise RuntimeError(
            "ADZUNA_APP_ID and ADZUNA_APP_KEY are not configured."
        )

    jobs = []

    # ========================================================
    # COLLECTION TIMESTAMP
    # ========================================================

    collected_at = datetime.now(
        timezone.utc
    ).isoformat()

    # ========================================================
    # COLLECT MULTIPLE PAGES
    # ========================================================

    for page in range(1, pages + 1):

        url = (
            f"{ADZUNA_BASE_URL}/jobs/"
            f"{country}/search/{page}"
        )

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": results_per_page,
            "what": role,
            "content-type": "application/json",
        }

        # ====================================================
        # OPTIONAL LOCATION FILTER
        # ====================================================

        if location:
            params["where"] = location

        # ====================================================
        # API REQUEST
        # ====================================================

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        # ====================================================
        # GET JOB RESULTS
        # ====================================================

        results = data.get(
            "results",
            []
        )

        if not results:
            break

        # ====================================================
        # CONVERT EACH JOB INTO JobPosting
        # ====================================================

        for item in results:

            location_data = item.get(
                "location",
                {}
            )

            company_data = item.get(
                "company",
                {}
            )

            category_data = item.get(
                "category",
                {}
            )

            job = JobPosting(

                # --------------------------------------------
                # SOURCE
                # --------------------------------------------

                source="adzuna",

                # --------------------------------------------
                # SOURCE JOB ID
                # --------------------------------------------

                source_job_id=str(
                    item.get(
                        "id",
                        ""
                    )
                ),

                # --------------------------------------------
                # JOB TITLE
                # --------------------------------------------

                title=item.get(
                    "title",
                    ""
                ),

                # --------------------------------------------
                # COMPANY
                # --------------------------------------------

                company=company_data.get(
                    "display_name",
                    ""
                ),

                # --------------------------------------------
                # LOCATION
                # --------------------------------------------

                location=location_data.get(
                    "display_name",
                    ""
                ),

                # --------------------------------------------
                # DESCRIPTION
                # --------------------------------------------

                description=item.get(
                    "description",
                    ""
                ),

                # --------------------------------------------
                # JOB URL
                # --------------------------------------------

                url=item.get(
                    "redirect_url",
                    ""
                ),

                # --------------------------------------------
                # CATEGORY
                # --------------------------------------------

                category=category_data.get(
                    "label",
                    ""
                ),

                # --------------------------------------------
                # SALARY
                # --------------------------------------------

                salary_min=item.get(
                    "salary_min"
                ),

                salary_max=item.get(
                    "salary_max"
                ),

                # --------------------------------------------
                # CONTRACT INFORMATION
                # --------------------------------------------

                contract_type=item.get(
                    "contract_type",
                    ""
                ),

                contract_time=item.get(
                    "contract_time",
                    ""
                ),

                # --------------------------------------------
                # ORIGINAL POSTING DATE
                # --------------------------------------------

                created_at=item.get(
                    "created",
                    ""
                ),

                # --------------------------------------------
                # OUR COLLECTION DATE
                # --------------------------------------------

                collected_at=collected_at,

                # --------------------------------------------
                # SEARCH QUERY
                # --------------------------------------------

                query=role,

                # --------------------------------------------
                # PAGE NUMBER
                # --------------------------------------------

                page=page,
            )

            jobs.append(job)

    return jobs


# ============================================================
# REMOVE DUPLICATE JOBS
# ============================================================

def remove_duplicate_jobs(
    jobs: list[JobPosting]
):
    """
    Remove exact duplicate postings
    using source + source_job_id.
    """

    unique_jobs = []

    seen = set()

    for job in jobs:

        key = (
            job.source,
            job.source_job_id
        )

        if key in seen:
            continue

        seen.add(key)

        unique_jobs.append(job)

    return unique_jobs