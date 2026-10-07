from .adzuna_collector import fetch_adzuna_jobs
from .processor import process_jobs
from .skill_extractor import (
    extract_skills_from_jobs,
    calculate_skill_demand,
    calculate_role_skill_demand,
)

from .database import (
    initialize_database,
    save_jobs,
    save_market_snapshot,
    start_market_run,
    complete_market_run,
)


# ============================================================
# SKILLFORAGE MARKET INTELLIGENCE PIPELINE
# ============================================================


def run_market_pipeline(
    role: str,
    country: str,
    pages: int = 3,
    results_per_page: int = 20,
    location: str = "",
):
    """
    Complete SkillForage Market Intelligence pipeline.

    Flow:

        Adzuna
            ↓
        Raw Jobs
            ↓
        Processing
            ↓
        Duplicate Removal
            ↓
        Role Normalization
            ↓
        Skill Extraction
            ↓
        Skill Demand
            ↓
        SQLite Database
            ↓
        Market Run
            ↓
        Market Snapshot
    """

    # ========================================================
    # STEP 0 — INITIALIZE DATABASE
    # ========================================================

    initialize_database()

    # ========================================================
    # CREATE RESEARCH / MARKET RUN
    # ========================================================

    run_id = start_market_run(
        source="adzuna",
        query_role=role,
        country=country,
        location=location,
    )

    print(
        f"\nMarket Run ID: {run_id}"
    )

    # ========================================================
    # STEP 1 — COLLECT JOBS
    # ========================================================

    print(
        "\n[1/6] Collecting jobs..."
    )

    try:

        raw_jobs = fetch_adzuna_jobs(
            role=role,
            country=country,
            pages=pages,
            results_per_page=results_per_page,
            location=location,
        )

        raw_job_count = len(
            raw_jobs
        )

        print(
            f"Collected {raw_job_count} jobs."
        )

        # ====================================================
        # STEP 2 — PROCESS JOBS
        # ====================================================

        print(
            "\n[2/6] Processing jobs..."
        )

        processed_jobs = process_jobs(
            raw_jobs
        )

        processed_job_count = len(
            processed_jobs
        )

        print(
            f"Processed {processed_job_count} jobs."
        )

        # ====================================================
        # STEP 3 — EXTRACT SKILLS
        # ====================================================

        print(
            "\n[3/6] Extracting skills..."
        )

        jobs_with_skills = (
            extract_skills_from_jobs(
                processed_jobs
            )
        )

        print(
            "Skill extraction completed."
        )

        # ====================================================
        # STEP 4 — CALCULATE OVERALL SKILL DEMAND
        # ====================================================

        print(
            "\n[4/6] Calculating skill demand..."
        )

        skill_demand = (
            calculate_skill_demand(
                jobs_with_skills
            )
        )

        # ====================================================
        # STEP 5 — ROLE-SPECIFIC DEMAND
        # ====================================================

        print(
            "\n[5/6] Calculating role-wise demand..."
        )

        normalized_roles = {}

        for job in jobs_with_skills:

            normalized_role = job.get(
                "normalized_role",
                "Other"
            )

            if normalized_role not in normalized_roles:

                normalized_roles[
                    normalized_role
                ] = []

            normalized_roles[
                normalized_role
            ].append(job)

        role_demand = {}

        for (
            normalized_role,
            role_jobs
        ) in normalized_roles.items():

            role_demand[
                normalized_role
            ] = calculate_role_skill_demand(
                role_jobs,
                normalized_role
            )

        # ====================================================
        # STEP 6 — SAVE TO DATABASE
        # ====================================================

        print(
            "\n[6/6] Saving market data..."
        )

        saved_job_ids = save_jobs(
            jobs_with_skills
        )

        # ====================================================
        # SAVE MARKET SNAPSHOTS
        # ====================================================

        for (
            normalized_role,
            demand
        ) in role_demand.items():

            save_market_snapshot(
                source="adzuna",
                query_role=role,
                normalized_role=normalized_role,
                skill_demand=demand,
                run_id=run_id,
            )

        # ====================================================
        # COMPLETE MARKET RUN
        # ====================================================

        complete_market_run(
            run_id=run_id,
            jobs_collected=raw_job_count,
            jobs_processed=processed_job_count,
            status="completed",
        )

        print(
            "Market data saved successfully."
        )

        print(
            f"Market Run {run_id} completed successfully."
        )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        return {

            "run_id":
                run_id,

            "query":
                role,

            "country":
                country,

            "location":
                location,

            "raw_job_count":
                raw_job_count,

            "processed_job_count":
                processed_job_count,

            "jobs":
                jobs_with_skills,

            "skill_demand":
                skill_demand,

            "role_skill_demand":
                role_demand,

            "saved_job_ids":
                saved_job_ids,
        }

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        complete_market_run(
            run_id=run_id,
            jobs_collected=locals().get(
                "raw_job_count",
                0
            ),
            jobs_processed=locals().get(
                "processed_job_count",
                0
            ),
            status="failed",
        )

        print(
            f"Market Run {run_id} failed."
        )

        raise error