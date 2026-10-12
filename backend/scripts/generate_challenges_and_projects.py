import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 4. CHALLENGES (Daily & Weekly)
# ------------------------------------------------------------------------------
CHALLENGES = [
    {
        "title": "Reverse Words in a String",
        "challenge_type": "daily",
        "skill_category": "Python",
        "description": "Given a sentence string, return a new string with the order of words reversed while preserving individual word characters.",
        "hints": [
            "Use string .split() to tokenize on whitespace",
            "Use slice notation [::-1] or .reverse() on the token list",
            "Join tokens back with ' '.join()"
        ],
        "xp_reward": 50,
        "solution_type": "code",
        "verification_rules": {"test_inputs": ["the sky is blue", "hello world"], "expected": ["blue is sky the", "world hello"]},
        "is_active": True
    },
    {
        "title": "SQL Aggregate Department Salary",
        "challenge_type": "daily",
        "skill_category": "SQL",
        "description": "Write a query selecting department_name and the average salary rounded to 2 decimal places from an employee table, filtering out departments with fewer than 3 staff members.",
        "hints": [
            "GROUP BY department_name",
            "Use ROUND(AVG(salary), 2)",
            "Filter aggregate counts using HAVING COUNT(*) >= 3"
        ],
        "xp_reward": 50,
        "solution_type": "quiz",
        "verification_rules": {"keyword_check": ["GROUP BY", "HAVING", "AVG"]},
        "is_active": True
    },
    {
        "title": "Find Duplicate Number in O(1) Space",
        "challenge_type": "daily",
        "skill_category": "DSA",
        "description": "Given an array of integers containing n + 1 integers where each integer is in range [1, n], find the single duplicate number using Floyd's Tortoise and Hare cycle detection in O(1) auxiliary space.",
        "hints": [
            "Treat array values as pointer indices into the array",
            "Phase 1: Advance slow by 1 step and fast by 2 steps until they intersect",
            "Phase 2: Reset slow to index 0 and advance both by 1 step until they meet"
        ],
        "xp_reward": 75,
        "solution_type": "code",
        "verification_rules": {"algorithm": "floyd_cycle_detection"},
        "is_active": True
    },
    {
        "title": "Build a Debounce Utility in JavaScript",
        "challenge_type": "weekly",
        "skill_category": "Web",
        "description": "Implement a `debounce(func, delay)` function that delays invoking `func` until after `delay` milliseconds have elapsed since the last time the debounced function was invoked.",
        "hints": [
            "Use setTimeout and clearTimeout inside a closure",
            "Return a function that resets the timer on every call",
            "Forward `this` context and arguments using .apply() or rest parameters"
        ],
        "xp_reward": 150,
        "solution_type": "code",
        "verification_rules": {"closure_check": True, "timer_cleared": True},
        "is_active": True
    },
    {
        "title": "Third Highest Salary with DENSE_RANK",
        "challenge_type": "weekly",
        "skill_category": "SQL",
        "description": "Write an ANSI SQL query utilizing window functions (DENSE_RANK) to extract employees earning the 3rd highest distinct compensation.",
        "hints": [
            "Use a Common Table Expression (CTE) or subquery",
            "Apply DENSE_RANK() OVER (ORDER BY salary DESC)",
            "Filter where rnk = 3 in the outer query"
        ],
        "xp_reward": 120,
        "solution_type": "code",
        "verification_rules": {"window_function": "DENSE_RANK"},
        "is_active": True
    },
    {
        "title": "Validate Balanced Parentheses Stack",
        "challenge_type": "daily",
        "skill_category": "DSA",
        "description": "Given a string containing '(', ')', '{', '}', '[' and ']', determine if the input string is valid using a Stack data structure.",
        "hints": [
            "Push opening brackets onto a stack",
            "When encountering a closing bracket, pop from stack and verify matching type",
            "Verify stack is empty at completion"
        ],
        "xp_reward": 50,
        "solution_type": "code",
        "verification_rules": {"test_inputs": ["()[]{}", "([)]"], "expected": [True, False]},
        "is_active": True
    },
    {
        "title": "Design a Rate Limiter Concept",
        "challenge_type": "weekly",
        "skill_category": "Problem Solving",
        "description": "Design a sliding window log rate limiter allowing maximum 60 requests per minute per user ID in distributed Redis.",
        "hints": [
            "Use a Redis Sorted Set (ZSET) per user",
            "Score and member are both current epoch timestamp in milliseconds",
            "Remove entries older than now - 60000ms using ZREMRANGEBYSCORE",
            "Check cardinality using ZCARD; if < 60, add request"
        ],
        "xp_reward": 150,
        "solution_type": "concept",
        "verification_rules": {"keywords": ["sorted set", "sliding window", "zremrangebyscore"]},
        "is_active": True
    },
    {
        "title": "Calculate Precision and Recall",
        "challenge_type": "daily",
        "skill_category": "Statistics/Data Analysis",
        "description": "Given True Positives = 40, False Positives = 10, False Negatives = 10, calculate Precision, Recall, and F1 Score.",
        "hints": [
            "Precision = TP / (TP + FP) = 40 / 50 = 0.80",
            "Recall = TP / (TP + FN) = 40 / 50 = 0.80",
            "F1 = 2 * (P * R) / (P + R) = 0.80"
        ],
        "xp_reward": 60,
        "solution_type": "quiz",
        "verification_rules": {"expected": 0.80},
        "is_active": True
    }
]

# ------------------------------------------------------------------------------
# 5. PROJECT TEMPLATES (12 Real-World Projects for Years 1-4)
# ------------------------------------------------------------------------------
PROJECT_TEMPLATES = [
    {
        "title": "Personal Portfolio & Interactive CLI Resume",
        "target_role": "frontend-engineer",
        "difficulty": "Beginner",
        "year_suitability": [1, 2],
        "problem_statement": "Students need a professional web presence and interactive CLI to demonstrate foundational coding, semantic HTML, modern responsive CSS, and Git version control.",
        "relevance": "Direct proof of basic web development fundamentals and clean documentation for early internship applications.",
        "skills": ["HTML", "CSS", "JavaScript", "Git", "Responsive Design"],
        "duration_hours": 15,
        "milestones": [
            {"id": "m1", "title": "Wireframe & Semantic Markup", "hours": 4},
            {"id": "m2", "title": "CSS Grid & Flexbox Styling", "hours": 5},
            {"id": "m3", "title": "Interactive DOM Interactions", "hours": 3},
            {"id": "m4", "title": "GitHub Pages Deployment", "hours": 3}
        ],
        "architecture": "Single-page responsive static architecture with modular CSS variables and clean vanilla JavaScript DOM controllers.",
        "datasets": ["Personal education, project descriptions, and verified skill badges."],
        "deliverables": ["Live GitHub Pages URL", "Public GitHub Repository with README", "Responsive layout across mobile/desktop"],
        "evaluation_checklist": [
            "Semantic HTML5 tags used throughout",
            "Zero horizontal overflow on mobile screens",
            "Valid Git commits with descriptive messages"
        ],
        "extensions": ["Add dark mode toggle using CSS custom properties", "Embed terminal-like interactive CLI prompt in canvas"]
    },
    {
        "title": "Student Career Analytics Dashboard",
        "target_role": "data-analyst",
        "difficulty": "Intermediate",
        "year_suitability": [2, 3],
        "problem_statement": "Analyze multi-year campus placement statistics and industry hiring trends to extract insights into top hiring branches, salary percentiles, and skill requirements.",
        "relevance": "Demonstrates data transformation with Python Pandas, SQL relational modeling, and interactive visualization in Power BI or Tableau.",
        "skills": ["Python", "SQL", "Pandas", "Power BI", "Statistics", "Data Visualization"],
        "duration_hours": 25,
        "milestones": [
            {"id": "m1", "title": "Dataset Cleaning & Normalization with Pandas", "hours": 6},
            {"id": "m2", "title": "SQL Schema Design & Analytical Queries", "hours": 7},
            {"id": "m3", "title": "Interactive Dashboard Creation in Power BI", "hours": 8},
            {"id": "m4", "title": "Executive Summary & Insights Report", "hours": 4}
        ],
        "architecture": "ETL pipeline loading raw placement CSVs into PostgreSQL/SQLite, running analytical SQL aggregations, and serving data to Power BI dashboards.",
        "datasets": ["Kaggle College Placement Dataset (synthetic student demographics, CGPA, technical test scores, and offers)."],
        "deliverables": ["Jupyter Notebook with EDA", "SQL aggregation script", "Power BI .pbix dashboard file & PDF report"],
        "evaluation_checklist": [
            "Handled missing values and outlier detection using IQR",
            "Calculated median, 75th percentile, and standard deviations by branch",
            "Built KPI cards and interactive cross-filtering visuals"
        ],
        "extensions": ["Implement automated daily CSV ingestion script", "Add salary predictive regression baseline"]
    },
    {
        "title": "High-Performance RESTful API with SQLite / Redis",
        "target_role": "backend-engineer",
        "difficulty": "Intermediate",
        "year_suitability": [2, 3, 4],
        "problem_statement": "Develop a production-ready, secure REST API service featuring user authentication, role-based access control, relational query pagination, and rate limiting.",
        "relevance": "Direct proof of backend competency: status codes, ORM modeling, transactional integrity, and OpenAPI compliance.",
        "skills": ["Python", "FastAPI", "SQL", "SQLAlchemy", "Redis", "Docker", "REST API"],
        "duration_hours": 30,
        "milestones": [
            {"id": "m1", "title": "Database Schema & Migration Setup", "hours": 6},
            {"id": "m2", "title": "Argon2 Password Hashing & JWT/Session Auth", "hours": 8},
            {"id": "m3", "title": "CRUD Endpoints with Pydantic Validation", "hours": 8},
            {"id": "m4", "title": "Automated Pytest Suite & Dockerfile", "hours": 8}
        ],
        "architecture": "Layered FastAPI architecture: Routers -> Services -> Repositories -> SQLAlchemy 2.0 ORM -> SQLite/Postgres.",
        "datasets": ["Custom synthetic e-commerce or LMS course catalog schema."],
        "deliverables": ["FastAPI source repository", "Interactive Swagger docs at /docs", "Pytest suite with >80% code coverage", "Dockerfile"],
        "evaluation_checklist": [
            "Strict Pydantic request and response schemas",
            "HTTP 401/403/404/422 status codes properly returned",
            "Foreign key cascading and indexes properly configured"
        ],
        "extensions": ["Add Redis caching layer for top read endpoints", "Implement GitHub Actions CI workflow"]
    },
    {
        "title": "Resume Keyword & ATS Optimization Engine",
        "target_role": "sde",
        "difficulty": "Advanced",
        "year_suitability": [3, 4],
        "problem_statement": "Create a deterministic text extraction and keyword matching engine that parses PDF resumes, tokenizes text, and computes job compatibility scores.",
        "relevance": "Highlights string processing, regex boundary handling, algorithm optimization, and PDF text extraction.",
        "skills": ["Python", "Algorithms", "pypdf", "Data Structures", "Problem Solving"],
        "duration_hours": 35,
        "milestones": [
            {"id": "m1", "title": "PDF Text Extraction Pipeline", "hours": 6},
            {"id": "m2", "title": "Taxonomy Matching with Word-Boundary Regex", "hours": 10},
            {"id": "m3", "title": "Scoring Engine & Feedback Heuristics", "hours": 10},
            {"id": "m4", "title": "CLI & Comprehensive Test Suite", "hours": 9}
        ],
        "architecture": "Text Processing Pipeline: PDF Ingestion -> Clean Text Normalizer -> Tokenizer -> Regex Boundary Matcher -> Scoring Aggregator.",
        "datasets": ["50+ open-source sample resume texts and job descriptions."],
        "deliverables": ["Modular Python package", "Evaluation script reporting precision and recall", "Clean CLI interface"],
        "evaluation_checklist": [
            "Accurately distinguishes 'Java' from 'JavaScript'",
            "Handles PDF corruption and multi-column formatting gracefully",
            "Calculates section completeness (Education, Skills, Experience)"
        ],
        "extensions": ["Add TF-IDF vector similarity comparison", "Export feedback report as downloadable PDF"]
    }
]

# ------------------------------------------------------------------------------
# 6. HACKATHONS (Demonstration data with verified dates and official links)
# ------------------------------------------------------------------------------
HACKATHONS = [
    {
        "name": "Smart India Hackathon 2026 (Student Edition)",
        "organizer": "Ministry of Education & AICTE",
        "mode": "hybrid",
        "location": "National / Multiple Nodal Centers",
        "date": "2026-11-15 to 2026-11-17",
        "deadline": "2026-10-31",
        "eligibility": "B.E., B.Tech, M.Tech, MCA, College Students",
        "description": "Nationwide competition providing students with a platform to solve pressing real-world problems facing government ministries and industries.",
        "official_link": "https://www.sih.gov.in/",
        "source": "Curated Student Competitions (Demo Entry)",
        "last_verified": "2026-10-10",
        "is_demo": True
    },
    {
        "name": "HackCBS 9.0 — Premier Student Hackathon",
        "organizer": "Shaheed Sukhdev College of Business Studies, Delhi University",
        "mode": "offline",
        "location": "New Delhi, India",
        "date": "2026-11-07 to 2026-11-08",
        "deadline": "2026-10-25",
        "eligibility": "Undergraduate Students (Any Branch / Year)",
        "description": "Annual 24-hour student hackathon fostering innovation in Web3, AI/ML, FinTech, and Open Innovation.",
        "official_link": "https://hackcbs.tech/",
        "source": "MLH / Student Hackathon Network (Demo Entry)",
        "last_verified": "2026-10-09",
        "is_demo": True
    },
    {
        "name": "HackVerse 2026 — National Technology Sprint",
        "organizer": "NITK Surathkal",
        "mode": "offline",
        "location": "Surathkal, Karnataka",
        "date": "2026-12-05 to 2026-12-06",
        "deadline": "2026-11-20",
        "eligibility": "All College Students (Year 1-4)",
        "description": "Flagship 36-hour hackathon bringing together innovative student developers and designers to build transformative digital products.",
        "official_link": "https://hackverse.nitk.ac.in/",
        "source": "Campus Innovation Portal (Demo Entry)",
        "last_verified": "2026-10-08",
        "is_demo": True
    },
    {
        "name": "Google Solution Challenge 2027 Preview",
        "organizer": "Google Developer Student Clubs (GDSC)",
        "mode": "online",
        "location": "Global / Virtual",
        "date": "2026-12-01 to 2027-01-31",
        "deadline": "2026-12-15",
        "eligibility": "GDSC College Members (All Majors)",
        "description": "Annual global contest challenging university students to solve one or more of the United Nations 17 Sustainable Development Goals using Google tech.",
        "official_link": "https://developers.google.com/community/gdsc-solution-challenge",
        "source": "Google Developers (Demo Entry)",
        "last_verified": "2026-10-11",
        "is_demo": True
    },
    {
        "name": "Flipkart GRiD 7.0 — Software Development Track",
        "organizer": "Flipkart Engineering",
        "mode": "online",
        "location": "Virtual (India)",
        "date": "2026-11-20 to 2026-12-10",
        "deadline": "2026-11-10",
        "eligibility": "B.Tech, B.E., M.Tech, Dual Degree Students",
        "description": "Flagship engineering challenge testing students on complex problems in system architecture, distributed queues, and algorithmic efficiency.",
        "official_link": "https://unstop.com/competitions/flipkart-grid",
        "source": "Unstop Tech Challenges (Demo Entry)",
        "last_verified": "2026-10-10",
        "is_demo": True
    }
]

with open(DATA_DIR / "challenges.json", "w", encoding="utf-8") as f:
    json.dump(CHALLENGES, f, indent=2)

with open(DATA_DIR / "project_templates.json", "w", encoding="utf-8") as f:
    json.dump(PROJECT_TEMPLATES, f, indent=2)

with open(DATA_DIR / "hackathons.json", "w", encoding="utf-8") as f:
    json.dump(HACKATHONS, f, indent=2)

print("Generated challenges.json, project_templates.json, and hackathons.json successfully!")
