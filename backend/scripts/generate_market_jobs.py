import json
from pathlib import Path
from datetime import datetime, timedelta
import random

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

COMPANIES = [
    "NovaTech Systems", "Apex Analytics", "CloudScale Labs", "Vanguard Infotech",
    "Starlight AI", "DataVerve Solutions", "QuantumSoft Inc.", "Horizon Dynamics",
    "Synapse HealthTech", "AeroByte Technologies", "Cognitive Wave", "FinEdge Global",
    "OmniData Corp", "NextEra Cloud", "TerraByte Analytics", "Hyperion CyberOps",
    "BlueShift Systems", "PixelCraft Studios", "MetricWise Solutions", "CoreStack Labs"
]

LOCATIONS = [
    "Bengaluru, Karnataka", "Hyderabad, Telangana", "Pune, Maharashtra",
    "Gurugram, Haryana", "Noida, Uttar Pradesh", "Chennai, Tamil Nadu",
    "Mumbai, Maharashtra", "Remote, India"
]

ROLES_DATA = [
    {
        "role": "Data Analyst",
        "category": "Data & Analytics",
        "skills": ["SQL", "Python", "Excel", "Power BI", "Statistics", "Data Visualization"],
        "min_sal": 450000, "max_sal": 900000,
        "desc_template": "Looking for a Data Analyst proficient in SQL, Python, and Power BI to analyze product usage, write complex SQL aggregations, and build executive dashboards."
    },
    {
        "role": "Data Scientist",
        "category": "Data & Analytics",
        "skills": ["Python", "Statistics", "Machine Learning", "Pandas", "Scikit-Learn", "SQL"],
        "min_sal": 700000, "max_sal": 1600000,
        "desc_template": "Seeking a Data Scientist with strong statistical foundations, predictive modeling experience in Scikit-Learn, and Python data manipulation skills."
    },
    {
        "role": "Machine Learning Engineer",
        "category": "AI & Engineering",
        "skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Docker", "REST API"],
        "min_sal": 900000, "max_sal": 2000000,
        "desc_template": "Join our AI team to deploy deep learning pipelines using PyTorch and FastAPI. Strong understanding of model optimization and Docker containerization required."
    },
    {
        "role": "Software Development Engineer",
        "category": "Software Engineering",
        "skills": ["Java", "C++", "Data Structures", "Algorithms", "Object Oriented Programming", "DBMS"],
        "min_sal": 800000, "max_sal": 1800000,
        "desc_template": "We are hiring SDE-1 candidates with exceptional DSA problem solving, solid OOP design skills in Java or C++, and knowledge of relational databases."
    },
    {
        "role": "Frontend Engineer",
        "category": "Web Development",
        "skills": ["JavaScript", "TypeScript", "React", "HTML", "CSS", "Tailwind CSS"],
        "min_sal": 600000, "max_sal": 1400000,
        "desc_template": "Frontend engineer needed to develop responsive, accessible React and TypeScript web applications with state management and Tailwind CSS styling."
    },
    {
        "role": "Backend Engineer",
        "category": "Web Development",
        "skills": ["Python", "Node.js", "FastAPI", "SQL", "PostgreSQL", "Redis", "REST API"],
        "min_sal": 750000, "max_sal": 1600000,
        "desc_template": "Backend developer to architect high-throughput REST APIs using FastAPI/Node.js, PostgreSQL relational schemas, and Redis caching."
    },
    {
        "role": "Full Stack Developer",
        "category": "Web Development",
        "skills": ["JavaScript", "React", "Node.js", "Python", "SQL", "HTML", "REST API"],
        "min_sal": 650000, "max_sal": 1500000,
        "desc_template": "Build features end-to-end across a modern React frontend and Node/Python backend with clean RESTful architecture and relational databases."
    },
    {
        "role": "Cloud Engineer",
        "category": "Cloud & Infrastructure",
        "skills": ["AWS", "Linux", "Terraform", "Docker", "Computer Networks", "Bash"],
        "min_sal": 700000, "max_sal": 1600000,
        "desc_template": "Manage cloud resources on AWS, automate infrastructure deployment with Terraform, and configure secure VPC networking and Linux instances."
    },
    {
        "role": "DevOps Engineer",
        "category": "Cloud & Infrastructure",
        "skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "Git", "Prometheus"],
        "min_sal": 800000, "max_sal": 1800000,
        "desc_template": "Automate deployment pipelines using GitHub Actions CI/CD, manage Kubernetes clusters, and set up Prometheus monitoring."
    },
    {
        "role": "Cybersecurity Analyst",
        "category": "Security",
        "skills": ["Computer Networks", "Linux", "Cybersecurity", "Python", "Operating Systems"],
        "min_sal": 650000, "max_sal": 1500000,
        "desc_template": "Monitor security threats, conduct vulnerability assessments, and inspect network traffic and authentication mechanisms."
    },
    {
        "role": "Database Administrator",
        "category": "Databases & Storage",
        "skills": ["SQL", "PostgreSQL", "MySQL", "DBMS", "Linux", "Operating Systems"],
        "min_sal": 700000, "max_sal": 1500000,
        "desc_template": "Manage production PostgreSQL and MySQL databases, optimize slow SQL queries with indexes, and administer backups."
    },
    {
        "role": "Product Manager",
        "category": "Product & Strategy",
        "skills": ["Product Management", "Agile", "Data Analysis", "SQL", "Problem Solving", "JIRA"],
        "min_sal": 900000, "max_sal": 2200000,
        "desc_template": "Drive product roadmap execution, define user stories and PRDs in JIRA, and analyze product metrics using SQL."
    },
    {
        "role": "QA Engineer",
        "category": "QA & Testing",
        "skills": ["Unit Testing", "Integration Testing", "Selenium", "Pytest", "Python", "Postman", "SQL"],
        "min_sal": 500000, "max_sal": 1100000,
        "desc_template": "Develop automated end-to-end regression tests using Selenium and Pytest, and conduct thorough REST API testing using Postman."
    }
]

EXPERIENCE_LEVELS = ["entry", "entry", "entry", "mid", "mid", "senior"]

JOB_POSTINGS = []
random.seed(42)  # Deterministic seed

base_date = datetime.utcnow()

# Generate 165 synthetic job postings (12-13 per role)
for role_idx, role_info in enumerate(ROLES_DATA):
    num_jobs = 13 if role_idx < 9 else 12
    for j in range(num_jobs):
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        exp = random.choice(EXPERIENCE_LEVELS)
        mult = 1.0 if exp == "entry" else (1.4 if exp == "mid" else 1.9)
        
        sal_min = round(role_info["min_sal"] * mult, -3)
        sal_max = round(role_info["max_sal"] * mult, -3)
        days_ago = random.randint(1, 45)
        posted_at = (base_date - timedelta(days=days_ago)).isoformat()
        
        # Select 4-6 skills from the role's skills
        sample_skills = random.sample(role_info["skills"], min(len(role_info["skills"]), random.randint(4, 6)))
        
        job_id = f"SYNTH_JOB_{role_idx + 1:02d}_{j + 1:02d}"
        job_title = f"{role_info['role']} ({exp.capitalize()} Level)"
        
        full_desc = (
            f"{role_info['desc_template']}\n\n"
            f"Key Requirements:\n"
            f"- Demonstrated practical ability in {', '.join(sample_skills)}.\n"
            f"- Understanding of modern software development life cycle.\n"
            f"- Strong problem solving and collaboration skills at {company}."
        )

        JOB_POSTINGS.append({
            "source": "synthetic_demo",
            "source_job_id": job_id,
            "title": job_title,
            "company": company,
            "location": location,
            "description": full_desc,
            "url": f"https://demo-jobs.skillforage.ai/postings/{job_id}",
            "category": role_info["category"],
            "salary_min": float(sal_min),
            "salary_max": float(sal_max),
            "experience_level": exp,
            "skills_extracted": sample_skills,
            "is_demo": True,
            "data_origin": "synthetic_demo",
            "posted_date": posted_at,
            "created_at": posted_at
        })

with open(DATA_DIR / "market_seed_jobs.json", "w", encoding="utf-8") as f:
    json.dump(JOB_POSTINGS, f, indent=2)

print(f"Generated {len(JOB_POSTINGS)} synthetic job postings in market_seed_jobs.json")
