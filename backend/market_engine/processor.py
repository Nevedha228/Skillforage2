import re
from difflib import SequenceMatcher

from .models import JobPosting


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:
    """
    Clean job-description text while preserving useful information.
    """

    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary special characters
    text = re.sub(r"[^\w\s.,+#/&()-]", " ", text)

    return text.strip()


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for comparison and duplicate detection.
    """

    text = text.lower().strip()

    text = re.sub(r"\s+", " ", text)

    return text


def normalize_company(company: str) -> str:
    """
    Normalize company names.
    """

    company = normalize_text(company)

    # Remove common company suffixes
    company = re.sub(
        r"\b(ltd|limited|pvt|private|inc|incorporated|llc|corp|corporation)\b",
        "",
        company
    )

    company = re.sub(r"[^a-z0-9\s]", " ", company)

    company = re.sub(r"\s+", " ", company)

    return company.strip()


# ============================================================
# ROLE NORMALIZATION
# ============================================================

ROLE_PATTERNS = {

    "Data Analyst": [
        r"\bdata analyst\b",
        r"\bdata analytics\b",
        r"\bbi analyst\b",
        r"\bbusiness intelligence analyst\b",
        r"\bpower bi analyst\b",
    ],

    "Data Scientist": [
        r"\bdata scientist\b",
        r"\bdata science\b",
        r"\bmachine learning scientist\b",
    ],

    "Machine Learning Engineer": [
        r"\bmachine learning engineer\b",
        r"\bml engineer\b",
        r"\bmachine learning developer\b",
    ],

    "Data Engineer": [
        r"\bdata engineer\b",
        r"\bbig data engineer\b",
        r"\bdata platform engineer\b",
    ],

    "Software Engineer": [
        r"\bsoftware engineer\b",
        r"\bsoftware developer\b",
        r"\bapplication developer\b",
        r"\bapplication engineer\b",
    ],

    "Backend Developer": [
        r"\bbackend developer\b",
        r"\bback end developer\b",
        r"\bbackend engineer\b",
        r"\bback end engineer\b",
    ],

    "Frontend Developer": [
        r"\bfrontend developer\b",
        r"\bfront end developer\b",
        r"\bfrontend engineer\b",
        r"\bfront end engineer\b",
    ],

    "Full Stack Developer": [
        r"\bfull stack developer\b",
        r"\bfullstack developer\b",
        r"\bfull stack engineer\b",
        r"\bfullstack engineer\b",
    ],

    "DevOps Engineer": [
        r"\bdevops engineer\b",
        r"\bdevops developer\b",
        r"\bsite reliability engineer\b",
        r"\bsre\b",
    ],

    "Cloud Engineer": [
        r"\bcloud engineer\b",
        r"\bcloud developer\b",
        r"\bcloud architect\b",
    ],

    "Cybersecurity Analyst": [
        r"\bcybersecurity analyst\b",
        r"\bsecurity analyst\b",
        r"\bcyber security analyst\b",
        r"\binformation security analyst\b",
    ],

    "Business Analyst": [
        r"\bbusiness analyst\b",
        r"\bbusiness systems analyst\b",
    ],

    "QA Engineer": [
        r"\bqa engineer\b",
        r"\bquality assurance engineer\b",
        r"\btest engineer\b",
        r"\bsoftware tester\b",
    ],
}


def normalize_role(title: str) -> str:
    """
    Convert many different job titles into a standardized role.
    """

    title_normalized = normalize_text(title)

    for role, patterns in ROLE_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, title_normalized):
                return role

    return "Other"


# ============================================================
# DUPLICATE DETECTION
# ============================================================

def similarity(text1: str, text2: str) -> float:
    """
    Calculate text similarity between 0 and 1.
    """

    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


def is_duplicate(job1: dict, job2: dict) -> bool:
    """
    Determine whether two job postings are likely duplicates.
    """

    # Same source + same job ID = definite duplicate
    if (
        job1.get("source")
        == job2.get("source")
        and job1.get("source_job_id")
        == job2.get("source_job_id")
        and job1.get("source_job_id")
    ):
        return True

    title1 = normalize_text(job1.get("title", ""))
    title2 = normalize_text(job2.get("title", ""))

    company1 = normalize_company(job1.get("company", ""))
    company2 = normalize_company(job2.get("company", ""))

    location1 = normalize_text(job1.get("location", ""))
    location2 = normalize_text(job2.get("location", ""))

    # Different companies are normally different jobs
    if company1 and company2 and company1 != company2:
        return False

    # Different titles are normally different jobs
    if title1 and title2 and title1 != title2:
        return False

    # Location must also match when both are available
    if location1 and location2 and location1 != location2:
        return False

    description1 = normalize_text(
        job1.get("description", "")
    )

    description2 = normalize_text(
        job2.get("description", "")
    )

    description_similarity = similarity(
        description1,
        description2
    )

    # Very similar descriptions strongly indicate duplication
    return description_similarity >= 0.90


# ============================================================
# JOB PROCESSING
# ============================================================

def process_jobs(jobs: list[JobPosting]) -> list[dict]:
    """
    Complete preprocessing pipeline:

    1. Clean text
    2. Remove invalid records
    3. Normalize job roles
    4. Remove duplicate postings
    """

    processed_jobs = []

    # --------------------------------------------------------
    # STEP 1: CLEAN
    # --------------------------------------------------------

    for job in jobs:

        title = clean_text(job.title)
        company = clean_text(job.company)
        location = clean_text(job.location)
        description = clean_text(job.description)

        # Ignore records without useful information
        if not title:
            continue

        if not description:
            continue

        processed_job = {
            "source": job.source,
            "source_job_id": job.source_job_id,

            "title": title,
            "company": company,
            "location": location,

            "description": description,

            "url": job.url,

            "category": clean_text(job.category),

            "salary_min": job.salary_min,
            "salary_max": job.salary_max,

            "contract_type": job.contract_type,
            "contract_time": job.contract_time,

            "created_at": job.created_at,
            "collected_at": job.collected_at,

            "query": job.query,
            "page": job.page,

            # NEW RESEARCH FIELDS
            "normalized_role": normalize_role(title),
            "duplicate_of": None,
        }

        processed_jobs.append(processed_job)

    # --------------------------------------------------------
    # STEP 2: DUPLICATE DETECTION
    # --------------------------------------------------------

    unique_jobs = []

    for current_job in processed_jobs:

        duplicate_found = False

        for existing_job in unique_jobs:

            if is_duplicate(
                current_job,
                existing_job
            ):
                current_job["duplicate_of"] = (
                    existing_job["source_job_id"]
                )

                duplicate_found = True
                break

        if not duplicate_found:
            unique_jobs.append(current_job)

    return unique_jobs


# ============================================================
# DATASET SUMMARY
# ============================================================

def summarize_jobs(jobs: list[dict]) -> dict:
    """
    Generate basic statistics about the processed dataset.
    """

    role_counts = {}

    for job in jobs:

        role = job.get(
            "normalized_role",
            "Other"
        )

        role_counts[role] = (
            role_counts.get(role, 0) + 1
        )

    return {
        "total_jobs": len(jobs),
        "role_distribution": role_counts,
    }