# ============================================================
# SKILLFORAGE
# SKILL EXTRACTION VALIDATION DATASET
# ============================================================
#
# Each job contains:
#
#   text           -> job posting text
#   expected_skills -> manually labelled ground truth
#
# The expected skills are what a human evaluator says
# are actually present in the job description.
#
# This dataset is used to evaluate the skill extractor.
# ============================================================


VALIDATION_DATASET = [

    # ========================================================
    # JOB 1 — DATA ANALYST
    # ========================================================

    {
        "id": "JOB_001",

        "text": """
        We are looking for a Data Analyst with strong SQL,
        Python, Excel and Power BI skills. The candidate should
        understand statistics and be able to build analytical
        dashboards.
        """,

        "expected_skills": [
            "SQL",
            "Python",
            "Excel",
            "Power BI",
            "Statistics",
        ],
    },


    # ========================================================
    # JOB 2 — DATA ANALYST
    # ========================================================

    {
        "id": "JOB_002",

        "text": """
        The Data Analyst will work with SQL databases,
        Microsoft Excel and Tableau to create business
        reports and dashboards.
        """,

        "expected_skills": [
            "SQL",
            "Excel",
            "Tableau",
        ],
    },


    # ========================================================
    # JOB 3 — MACHINE LEARNING
    # ========================================================

    {
        "id": "JOB_003",

        "text": """
        The Machine Learning Engineer should have strong
        Python programming skills and experience with
        Pandas, NumPy and Scikit-learn.
        """,

        "expected_skills": [
            "Machine Learning",
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
        ],
    },


    # ========================================================
    # JOB 4 — SOFTWARE ENGINEER
    # ========================================================

    {
        "id": "JOB_004",

        "text": """
        Software Engineer required with Java programming,
        object oriented programming, data structures,
        algorithms and SQL knowledge.
        """,

        "expected_skills": [
            "Java",
            "Object-Oriented Programming",
            "Data Structures",
            "Algorithms",
            "SQL",
        ],
    },


    # ========================================================
    # JOB 5 — FRONTEND DEVELOPER
    # ========================================================

    {
        "id": "JOB_005",

        "text": """
        Frontend Developer required with strong JavaScript,
        React, HTML and CSS experience.
        """,

        "expected_skills": [
            "JavaScript",
            "React",
            "HTML",
            "CSS",
        ],
    },


    # ========================================================
    # JOB 6 — CLOUD / DEVOPS
    # ========================================================

    {
        "id": "JOB_006",

        "text": """
        Cloud Engineer should have experience with AWS,
        Docker, Kubernetes and Git.
        """,

        "expected_skills": [
            "AWS",
            "Docker",
            "Kubernetes",
            "Git",
        ],
    },


    # ========================================================
    # JOB 7 — NLP / AI
    # ========================================================

    {
        "id": "JOB_007",

        "text": """
        AI Engineer with Python experience and knowledge
        of machine learning, natural language processing
        and TensorFlow.
        """,

        "expected_skills": [
            "Python",
            "Machine Learning",
            "Natural Language Processing",
            "TensorFlow",
        ],
    },


    # ========================================================
    # JOB 8 — BACKEND DEVELOPER
    # ========================================================

    {
        "id": "JOB_008",

        "text": """
        Backend Developer required with Python, FastAPI,
        REST API, PostgreSQL and Docker experience.
        """,

        "expected_skills": [
            "Python",
            "FastAPI",
            "REST API",
            "PostgreSQL",
            "Docker",
        ],
    },


    # ========================================================
    # JOB 9 — DATA ANALYST
    # ========================================================

    {
        "id": "JOB_009",

        "text": """
        Data Analyst with experience in R programming,
        SQL, Tableau and statistical analysis.
        """,

        "expected_skills": [
            "R",
            "SQL",
            "Tableau",
            "Statistics",
        ],
    },


    # ========================================================
    # JOB 10 — DATABASE DEVELOPER
    # ========================================================

    {
        "id": "JOB_010",

        "text": """
        Database Developer should have experience writing
        SQL queries and working with MySQL databases.
        """,

        "expected_skills": [
            "SQL",
            "MySQL",
        ],
    },

]