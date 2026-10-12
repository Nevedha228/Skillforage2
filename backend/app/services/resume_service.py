import re
import os
import io
from typing import Dict, Any, List, Optional
from datetime import datetime
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models import UserResume
from app.schemas.resume import ATSAnalysisResponse, ResumeStructuredData

ATS_DISCLAIMER = (
    "Disclaimer: The ATS compatibility score is an automated heuristic estimate evaluating standard section "
    "headers, readability, and technical keyword density. Real Applicant Tracking Systems and human recruiters "
    "employ diverse parsing criteria; this score is an optimization guide and not a hiring guarantee."
)

STANDARD_KEYWORDS = [
    "python", "java", "sql", "javascript", "react", "html", "css", "c++", "git", "github",
    "fastapi", "spring boot", "rest api", "mysql", "postgresql", "mongodb", "docker", "aws",
    "linux", "data structures", "algorithms", "oop", "dbms", "machine learning", "statistics",
    "pandas", "numpy", "power bi", "excel", "unit testing", "ci/cd", "agile", "problem solving"
]

def extract_text_from_pdf_stream(stream: io.BytesIO) -> str:
    """Extract text safely from in-memory PDF stream using pypdf."""
    try:
        reader = PdfReader(stream)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts).strip()
    except Exception as e:
        return ""


def parse_resume_sections(text: str) -> Dict[str, Any]:
    """Parse resume text into structured sections."""
    text_lower = text.lower()

    # Section patterns
    def extract_between(headings: List[str], next_headings: List[str]) -> str:
        for h in headings:
            pattern = rf"(?:^|\n)\s*{re.escape(h)}\s*:?\s*\n(.*?)(?=\n\s*(?:{'|'.join(re.escape(nh) for nh in next_headings)})\s*:?|\Z)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    education_text = extract_between(["education", "academic background"], ["technical skills", "skills", "projects", "experience"])
    skills_text = extract_between(["technical skills", "skills", "technologies"], ["projects", "experience", "internships", "achievements"])
    projects_text = extract_between(["projects", "key projects", "academic projects"], ["experience", "internships", "certifications", "achievements"])
    experience_text = extract_between(["experience", "work experience", "internships"], ["projects", "certifications", "achievements", "education"])
    summary_text = extract_between(["summary", "professional summary", "about me"], ["education", "skills", "technical skills", "projects"])

    # Extract detected skills from skills_text or entire resume
    skills_list = []
    for kw in STANDARD_KEYWORDS:
        pattern = rf"\b{re.escape(kw)}\b"
        if re.search(pattern, text_lower):
            skills_list.append(kw.title() if len(kw) > 3 else kw.upper())

    # Format structured sections
    return {
        "summary": summary_text or "Motivated student seeking technical opportunities to apply engineering skills.",
        "education": [{"degree": "Degree / Course", "details": education_text[:300]}] if education_text else [],
        "skills": list(set(skills_list)),
        "projects": [{"title": "Project Highlight", "description": projects_text[:400]}] if projects_text else [],
        "experience": [{"role": "Internship / Experience", "description": experience_text[:400]}] if experience_text else [],
        "achievements": []
    }


def analyze_ats_heuristics(text: str, job_desc: Optional[str] = None) -> ATSAnalysisResponse:
    text_lower = text.lower() if text else ""

    # 1. Section presence checks
    sections = {
        "Contact Information": bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text_lower)),
        "Summary": any(h in text_lower for h in ["summary", "profile", "objective", "about"]),
        "Education": any(h in text_lower for h in ["education", "b.tech", "b.e.", "bca", "degree", "university", "college"]),
        "Technical Skills": any(h in text_lower for h in ["skills", "technical skills", "technologies", "competencies"]),
        "Projects": any(h in text_lower for h in ["project", "projects", "capstone"]),
        "Experience / Internships": any(h in text_lower for h in ["experience", "internship", "intern", "employment"])
    }

    # 2. Keyword check
    found_keywords = []
    missing_keywords = []
    for kw in STANDARD_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", text_lower):
            found_keywords.append(kw.title() if len(kw) > 3 else kw.upper())
        else:
            missing_keywords.append(kw.title() if len(kw) > 3 else kw.upper())

    # 3. Score calculation
    section_score = (sum(1 for v in sections.values() if v) / len(sections)) * 50
    keyword_score = min(50.0, (len(found_keywords) / 12.0) * 50)
    total_ats = int(round(section_score + keyword_score))
    total_ats = max(15, min(98, total_ats))

    # Suggestions (honest, never fabricate experience)
    suggestions = []
    if not sections["Summary"]:
        suggestions.append("Add a concise 2-3 sentence Professional Summary highlighting your career goals and core strengths.")
    if not sections["Projects"]:
        suggestions.append("Include at least 2 technical projects detailing problem statements, architecture, and tools used.")
    if not sections["Experience / Internships"]:
        suggestions.append("If you have completed college club leadership, open source contributions, or internships, include them in an Experience section.")
    if len(found_keywords) < 6:
        suggestions.append("Incorporate specific technical tool and language names relevant to your target role.")

    # 4. Job Description comparison
    job_match_score = None
    missing_jd_keywords = None
    if job_desc and job_desc.strip():
        jd_lower = job_desc.lower()
        jd_keywords = [kw for kw in STANDARD_KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", jd_lower)]
        if jd_keywords:
            matched_jd = [kw for kw in jd_keywords if re.search(rf"\b{re.escape(kw)}\b", text_lower)]
            missing_jd = [kw for kw in jd_keywords if kw not in matched_jd]

            job_match_score = int(round((len(matched_jd) / len(jd_keywords)) * 100))
            missing_jd_keywords = [kw.title() if len(kw) > 3 else kw.upper() for kw in missing_jd]
            suggestions.append(f"Your resume matches {len(matched_jd)} of {len(jd_keywords)} detected keywords from the job description.")

    return ATSAnalysisResponse(
        ats_score_estimate=total_ats,
        disclaimer=ATS_DISCLAIMER,
        section_presence=sections,
        found_keywords=found_keywords[:15],
        missing_keywords=missing_keywords[:12],
        suggestions=suggestions,
        job_match_score=job_match_score,
        missing_job_keywords=missing_jd_keywords
    )
