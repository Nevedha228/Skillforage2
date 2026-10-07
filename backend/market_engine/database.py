import sqlite3
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "market_data.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # ========================================================
    # JOBS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source TEXT NOT NULL,
            source_job_id TEXT NOT NULL,

            title TEXT NOT NULL,
            normalized_role TEXT,

            company TEXT,
            location TEXT,
            description TEXT,

            url TEXT,
            category TEXT,

            salary_min REAL,
            salary_max REAL,

            contract_type TEXT,
            contract_time TEXT,

            created_at TEXT,
            collected_at TEXT,

            query TEXT,
            page INTEGER,

            created_in_database_at TEXT,

            UNIQUE(source, source_job_id)
        )
    """)

    # ========================================================
    # SKILLS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            skill_name TEXT NOT NULL UNIQUE,
            category TEXT
        )
    """)

    # ========================================================
    # JOB-SKILLS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,

            evidence TEXT,

            PRIMARY KEY(job_id, skill_id),

            FOREIGN KEY(job_id)
                REFERENCES jobs(id)
                ON DELETE CASCADE,

            FOREIGN KEY(skill_id)
                REFERENCES skills(id)
                ON DELETE CASCADE
        )
    """)

    # ========================================================
    # MARKET RUNS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source TEXT NOT NULL,

            query_role TEXT,
            country TEXT,
            location TEXT,

            started_at TEXT NOT NULL,
            completed_at TEXT,

            jobs_collected INTEGER DEFAULT 0,
            jobs_processed INTEGER DEFAULT 0,

            status TEXT DEFAULT 'running'
        )
    """)

    # ========================================================
    # MARKET SNAPSHOTS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            snapshot_date TEXT NOT NULL,

            source TEXT,
            query_role TEXT,
            normalized_role TEXT,

            skill_name TEXT,

            job_count INTEGER,
            total_jobs INTEGER,

            demand_percentage REAL
        )
    """)

    # ========================================================
    # MIGRATION
    # ========================================================

    cursor.execute("""
        PRAGMA table_info(market_snapshots)
    """)

    columns = cursor.fetchall()

    existing_columns = [
        column["name"]
        for column in columns
    ]

    if "run_id" not in existing_columns:

        cursor.execute("""
            ALTER TABLE market_snapshots
            ADD COLUMN run_id INTEGER
        """)

    # ========================================================
    # INDEXES
    # ========================================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_jobs_role
        ON jobs(normalized_role)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_jobs_collected_at
        ON jobs(collected_at)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_job_skills_skill
        ON job_skills(skill_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_snapshots_role_date
        ON market_snapshots(
            normalized_role,
            snapshot_date
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_snapshots_run
        ON market_snapshots(run_id)
    """)

    connection.commit()
    connection.close()


# ============================================================
# START MARKET RUN
# ============================================================

def start_market_run(
    source,
    query_role="",
    country="",
    location=""
):

    connection = get_connection()
    cursor = connection.cursor()

    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute("""
        INSERT INTO market_runs (
            source,
            query_role,
            country,
            location,
            started_at,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        source,
        query_role,
        country,
        location,
        started_at,
        "running"
    ))

    run_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return run_id


# ============================================================
# COMPLETE MARKET RUN
# ============================================================

def complete_market_run(
    run_id,
    jobs_collected,
    jobs_processed,
    status="completed"
):

    connection = get_connection()
    cursor = connection.cursor()

    completed_at = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute("""
        UPDATE market_runs
        SET
            completed_at = ?,
            jobs_collected = ?,
            jobs_processed = ?,
            status = ?
        WHERE id = ?
    """, (
        completed_at,
        jobs_collected,
        jobs_processed,
        status,
        run_id
    ))

    connection.commit()
    connection.close()


# ============================================================
# GET MARKET RUNS
# ============================================================

def get_market_runs():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            source,
            query_role,
            country,
            location,
            started_at,
            completed_at,
            jobs_collected,
            jobs_processed,
            status
        FROM market_runs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# GET OR CREATE SKILL
# ============================================================

def get_or_create_skill(
    skill_name,
    category=""
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM skills
        WHERE skill_name = ?
    """, (
        skill_name,
    ))

    row = cursor.fetchone()

    if row:

        skill_id = row["id"]

    else:

        cursor.execute("""
            INSERT INTO skills (
                skill_name,
                category
            )
            VALUES (?, ?)
        """, (
            skill_name,
            category
        ))

        skill_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return skill_id


# ============================================================
# SAVE JOB
#
# Supports the EXACT format used by test_database.py
# ============================================================

def save_job(job):

    connection = get_connection()
    cursor = connection.cursor()

    created_in_database_at = datetime.now(
        timezone.utc
    ).isoformat()

    # ========================================================
    # GET JOB INFORMATION
    # ========================================================

    source = job.get(
        "source",
        ""
    )

    source_job_id = job.get(
        "source_job_id",
        ""
    )

    title = job.get(
        "title",
        ""
    )

    normalized_role = job.get(
        "normalized_role",
        ""
    )

    company = job.get(
        "company",
        ""
    )

    location = job.get(
        "location",
        ""
    )

    description = job.get(
        "description",
        ""
    )

    url = job.get(
        "url",
        ""
    )

    category = job.get(
        "category",
        ""
    )

    salary_min = job.get(
        "salary_min",
        None
    )

    salary_max = job.get(
        "salary_max",
        None
    )

    contract_type = job.get(
        "contract_type",
        ""
    )

    contract_time = job.get(
        "contract_time",
        ""
    )

    created_at = job.get(
        "created_at",
        ""
    )

    collected_at = job.get(
        "collected_at",
        ""
    )

    query = job.get(
        "query",
        ""
    )

    page = job.get(
        "page",
        1
    )

    # ========================================================
    # INSERT JOB
    # ========================================================

    cursor.execute("""
        INSERT OR IGNORE INTO jobs (
            source,
            source_job_id,
            title,
            normalized_role,
            company,
            location,
            description,
            url,
            category,
            salary_min,
            salary_max,
            contract_type,
            contract_time,
            created_at,
            collected_at,
            query,
            page,
            created_in_database_at
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        source,
        source_job_id,
        title,
        normalized_role,
        company,
        location,
        description,
        url,
        category,
        salary_min,
        salary_max,
        contract_type,
        contract_time,
        created_at,
        collected_at,
        query,
        page,
        created_in_database_at
    ))

    # ========================================================
    # GET JOB ID
    # ========================================================

    cursor.execute("""
        SELECT id
        FROM jobs
        WHERE source = ?
        AND source_job_id = ?
    """, (
        source,
        source_job_id
    ))

    row = cursor.fetchone()

    if row is None:

        connection.close()

        raise RuntimeError(
            "Could not retrieve saved job ID."
        )

    job_id = row["id"]

    # ========================================================
    # GET SKILLS FROM TEST JOB / REAL JOB
    # ========================================================

    skills = job.get(
        "skills",
        []
    )

    skill_evidence = job.get(
        "skill_evidence",
        {}
    )

    # ========================================================
    # SAVE SKILLS
    # ========================================================

    for skill_name in skills:

        if not skill_name:
            continue

        evidence = skill_evidence.get(
            skill_name,
            ""
        )

        # ----------------------------------------------------
        # Find skill
        # ----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM skills
            WHERE skill_name = ?
        """, (
            skill_name,
        ))

        skill_row = cursor.fetchone()

        # ----------------------------------------------------
        # Create skill
        # ----------------------------------------------------

        if skill_row:

            skill_id = skill_row["id"]

        else:

            cursor.execute("""
                INSERT INTO skills (
                    skill_name,
                    category
                )
                VALUES (?, ?)
            """, (
                skill_name,
                ""
            ))

            skill_id = cursor.lastrowid

        # ----------------------------------------------------
        # Connect job + skill
        # ----------------------------------------------------

        cursor.execute("""
            INSERT OR IGNORE INTO job_skills (
                job_id,
                skill_id,
                evidence
            )
            VALUES (?, ?, ?)
        """, (
            job_id,
            skill_id,
            evidence
        ))

    # ========================================================
    # COMMIT
    # ========================================================

    connection.commit()
    connection.close()

    return job_id


# ============================================================
# SAVE MULTIPLE JOBS
#
# This version supports:
#
# [(job, skills)]
#
# and also:
#
# [job]
# ============================================================

def save_jobs(jobs):

    saved_ids = []

    for item in jobs:

        # ----------------------------------------------------
        # If pipeline gives (job, skills)
        # ----------------------------------------------------

        if (
            isinstance(item, tuple)
            and len(item) == 2
        ):

            job = item[0]
            skills = item[1]

            # Make a copy if it's a dictionary
            if isinstance(job, dict):

                job_data = job.copy()

                if "skills" not in job_data:
                    job_data["skills"] = skills

            else:

                job_data = job

        # ----------------------------------------------------
        # If pipeline gives just job
        # ----------------------------------------------------

        else:

            job_data = item

        job_id = save_job(
            job_data
        )

        saved_ids.append(
            job_id
        )

    return saved_ids


# ============================================================
# SAVE MARKET SNAPSHOT
# ============================================================

def save_market_snapshot(
    source,
    query_role,
    normalized_role,
    skill_demand,
    run_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    snapshot_date = datetime.now(
        timezone.utc
    ).date().isoformat()

    for item in skill_demand:

        cursor.execute("""
            INSERT INTO market_snapshots (
                run_id,
                snapshot_date,
                source,
                query_role,
                normalized_role,
                skill_name,
                job_count,
                total_jobs,
                demand_percentage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            snapshot_date,
            source,
            query_role,
            normalized_role,
            item["skill"],
            item["job_count"],
            item["total_jobs"],
            item["demand_percentage"]
        ))

    connection.commit()
    connection.close()


# ============================================================
# DATABASE STATISTICS
# ============================================================

def get_database_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Jobs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM jobs
    """)

    jobs = cursor.fetchone()["count"]

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM skills
    """)

    skills = cursor.fetchone()["count"]

    # --------------------------------------------------------
    # Job-skill relationships
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM job_skills
    """)

    job_skills = cursor.fetchone()["count"]

    # --------------------------------------------------------
    # Market snapshots
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM market_snapshots
    """)

    snapshots = cursor.fetchone()["count"]

    # --------------------------------------------------------
    # Market runs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM market_runs
    """)

    market_runs = cursor.fetchone()["count"]

    connection.close()

    return {
        "jobs": jobs,
        "skills": skills,

        # IMPORTANT:
        # Your test_database.py expects this exact key.
        "job_skills": job_skills,

        "market_snapshots": snapshots,
        "market_runs": market_runs
    }