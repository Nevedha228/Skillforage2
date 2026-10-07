import sqlite3
from .database import get_connection


# ============================================================
# SKILLFORAGE MARKET ANALYTICS
# ============================================================


# ============================================================
# 1. TOP SKILLS
# ============================================================

def get_top_skills(
    limit: int = 10,
    normalized_role: str = ""
):
    """
    Return the most frequently demanded skills.

    If normalized_role is provided,
    results are restricted to that role.

    Role matching is case-insensitive.
    Example:
        data analyst
        Data Analyst
        DATA ANALYST

    All are treated as the same role.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if normalized_role:

        cursor.execute(
            """
            SELECT
                s.skill_name,
                s.category,
                COUNT(DISTINCT js.job_id) AS job_count
            FROM skills s

            JOIN job_skills js
                ON s.id = js.skill_id

            JOIN jobs j
                ON j.id = js.job_id

            WHERE LOWER(TRIM(j.normalized_role))
                  = LOWER(TRIM(?))

            GROUP BY
                s.id,
                s.skill_name,
                s.category

            ORDER BY
                job_count DESC,
                s.skill_name ASC

            LIMIT ?
            """,
            (
                normalized_role,
                limit
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                s.skill_name,
                s.category,
                COUNT(DISTINCT js.job_id) AS job_count
            FROM skills s

            JOIN job_skills js
                ON s.id = js.skill_id

            GROUP BY
                s.id,
                s.skill_name,
                s.category

            ORDER BY
                job_count DESC,
                s.skill_name ASC

            LIMIT ?
            """,
            (limit,)
        )

    rows = cursor.fetchall()

    # --------------------------------------------------------
    # Get denominator
    # --------------------------------------------------------

    if normalized_role:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE LOWER(TRIM(normalized_role))
                  = LOWER(TRIM(?))
            """,
            (normalized_role,)
        )

    else:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            """
        )

    total_jobs = cursor.fetchone()[0]

    connection.close()

    results = []

    for row in rows:

        demand_percentage = 0

        if total_jobs > 0:

            demand_percentage = (
                row["job_count"]
                / total_jobs
            ) * 100

        results.append(
            {
                "skill": row["skill_name"],

                "category": row["category"],

                "job_count": row["job_count"],

                "total_jobs": total_jobs,

                "demand_percentage": round(
                    demand_percentage,
                    2
                ),
            }
        )

    return results


# ============================================================
# 2. ROLE DISTRIBUTION
# ============================================================

def get_role_distribution():
    """
    Count how many collected jobs belong
    to each normalized role.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            normalized_role,
            COUNT(*) AS job_count
        FROM jobs

        WHERE normalized_role IS NOT NULL
        AND TRIM(normalized_role) != ''

        GROUP BY normalized_role

        ORDER BY job_count DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": row["normalized_role"],
            "job_count": row["job_count"],
        }
        for row in rows
    ]


# ============================================================
# 3. ROLE-WISE TOP SKILLS
# ============================================================

def get_role_skill_analysis(
    role: str,
    limit: int = 10
):
    """
    Return the most demanded skills
    for a specific role.

    Role matching is case-insensitive.
    """

    return get_top_skills(
        limit=limit,
        normalized_role=role
    )


# ============================================================
# 4. SALARY ANALYSIS
# ============================================================

def get_salary_analysis(
    normalized_role: str = ""
):
    """
    Calculate basic salary statistics
    from available salary values.

    Role matching is case-insensitive.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if normalized_role:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS jobs_with_salary,

                AVG(salary_min) AS avg_salary_min,

                AVG(salary_max) AS avg_salary_max,

                MIN(salary_min) AS min_salary,

                MAX(salary_max) AS max_salary

            FROM jobs

            WHERE LOWER(TRIM(normalized_role))
                  = LOWER(TRIM(?))

            AND (
                salary_min IS NOT NULL
                OR salary_max IS NOT NULL
            )
            """,
            (normalized_role,)
        )

    else:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS jobs_with_salary,

                AVG(salary_min) AS avg_salary_min,

                AVG(salary_max) AS avg_salary_max,

                MIN(salary_min) AS min_salary,

                MAX(salary_max) AS max_salary

            FROM jobs

            WHERE
                salary_min IS NOT NULL
                OR salary_max IS NOT NULL
            """
        )

    row = cursor.fetchone()

    connection.close()

    return {
        "jobs_with_salary":
            row["jobs_with_salary"],

        "average_min_salary":
            round(
                row["avg_salary_min"],
                2
            )
            if row["avg_salary_min"]
            is not None
            else None,

        "average_max_salary":
            round(
                row["avg_salary_max"],
                2
            )
            if row["avg_salary_max"]
            is not None
            else None,

        "minimum_salary":
            row["min_salary"],

        "maximum_salary":
            row["max_salary"],
    }


# ============================================================
# 5. LOCATION DISTRIBUTION
# ============================================================

def get_location_distribution(
    limit: int = 10
):
    """
    Return locations containing the
    largest number of collected jobs.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            location,
            COUNT(*) AS job_count

        FROM jobs

        WHERE location IS NOT NULL
        AND TRIM(location) != ''

        GROUP BY location

        ORDER BY job_count DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "location": row["location"],
            "job_count": row["job_count"],
        }
        for row in rows
    ]


# ============================================================
# 6. MARKET SNAPSHOT HISTORY
# ============================================================

def get_market_snapshots(
    role: str = "",
    skill: str = ""
):
    """
    Retrieve historical market snapshots.

    Role matching is case-insensitive.

    This will later power trend charts.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            snapshot_date,
            source,
            query_role,
            normalized_role,
            skill_name,
            job_count,
            total_jobs,
            demand_percentage

        FROM market_snapshots

        WHERE 1 = 1
    """

    parameters = []

    if role:

        query += """
            AND LOWER(TRIM(normalized_role))
                = LOWER(TRIM(?))
        """

        parameters.append(role)

    if skill:

        query += """
            AND LOWER(TRIM(skill_name))
                = LOWER(TRIM(?))
        """

        parameters.append(skill)

    query += """
        ORDER BY
            snapshot_date ASC,
            skill_name ASC
    """

    cursor.execute(
        query,
        parameters
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# 7. COMPLETE MARKET SUMMARY
# ============================================================

def get_market_summary(
    role: str = ""
):
    """
    Return a complete market intelligence summary.

    Role matching is case-insensitive.
    """

    return {

        "role": role,

        "top_skills":
            get_top_skills(
                limit=10,
                normalized_role=role
            ),

        "salary":
            get_salary_analysis(
                normalized_role=role
            ),

        "locations":
            get_location_distribution(
                limit=10
            ),

        "snapshots":
            get_market_snapshots(
                role=role
            ),
    }