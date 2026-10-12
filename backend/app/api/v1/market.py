from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
import json
import csv
import io

from app.database.database import get_db
from app.core.deps import get_current_user, get_optional_user
from app.core.config import settings
from app.models import User, JobPosting
from app.services.market_service import get_market_analytics_summary, compare_user_skill_gap
from market_engine.skill_extractor import extract_skills

router = APIRouter(prefix="/market", tags=["Market Intelligence & Skill Gap"])

@router.get("/analytics")
def get_market_analytics(
    data_origin: str = Query("synthetic_demo"),  # "synthetic_demo", "collected", "imported", "all"
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Returns aggregated labor market intelligence statistics.
    Every response is strictly labeled with its data origin.
    Never blends synthetic demo data into real collected statistics without explicit notice.
    """
    return get_market_analytics_summary(data_origin=data_origin, role_filter=role, db=db)


@router.get("/skill-gap")
def get_student_skill_gap(
    role_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target = role_id or current_user.target_role or "sde"
    return compare_user_skill_gap(current_user.id, target, db)


@router.post("/import")
async def import_job_postings(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Imports job postings from CSV or JSON file.
    All imported postings are strictly flagged data_origin='imported'.
    """
    content = await file.read()
    filename = file.filename.lower() if file.filename else ""
    created_count = 0

    try:
        if filename.endswith(".json"):
            data = json.loads(content.decode("utf-8"))
            if not isinstance(data, list):
                data = [data]
            for item in data:
                desc = item.get("description", "")
                skills = item.get("skills_extracted") or extract_skills(desc)
                job = JobPosting(
                    source="imported_file",
                    source_job_id=item.get("id") or item.get("source_job_id"),
                    title=item.get("title", "Job Title"),
                    company=item.get("company", "Company"),
                    location=item.get("location", "Remote"),
                    description=desc,
                    url=item.get("url"),
                    category=item.get("category", "Software Engineering"),
                    salary_min=item.get("salary_min"),
                    salary_max=item.get("salary_max"),
                    experience_level=item.get("experience_level", "entry"),
                    skills_extracted=skills,
                    is_demo=False,
                    data_origin="imported"
                )
                db.add(job)
                created_count += 1
        elif filename.endswith(".csv"):
            csv_text = content.decode("utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(csv_text))
            for row in reader:
                desc = row.get("description", "")
                skills = extract_skills(desc)
                job = JobPosting(
                    source="imported_csv",
                    source_job_id=row.get("id") or row.get("job_id"),
                    title=row.get("title", "Job Title"),
                    company=row.get("company", "Company"),
                    location=row.get("location", "Remote"),
                    description=desc,
                    url=row.get("url"),
                    category=row.get("category", "Software Engineering"),
                    skills_extracted=skills,
                    is_demo=False,
                    data_origin="imported"
                )
                db.add(job)
                created_count += 1
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Please upload a .json or .csv file."
            )

        db.commit()
        return {
            "success": True,
            "imported_count": created_count,
            "data_origin": "imported",
            "message": f"Successfully ingested {created_count} job postings labeled as 'imported'."
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse import file: {str(e)}"
        )


@router.get("/status")
def get_external_adapters_status():
    """
    Honesty Rule: Clearly reports live external adapter configuration status.
    """
    has_adzuna = bool(settings.ADZUNA_APP_ID and settings.ADZUNA_APP_KEY)
    has_llm = bool(settings.LLM_API_KEY)
    has_smtp = bool(settings.SMTP_HOST)

    return {
        "integrations": {
            "adzuna_api": {
                "status": "connected" if has_adzuna else "not_configured",
                "description": "Live labor market data collection via Adzuna API"
            },
            "llm_service": {
                "status": "connected" if has_llm else "not_configured",
                "description": "Natural language feedback for mock interviews"
            },
            "email_smtp": {
                "status": "connected" if has_smtp else "development_console_fallback",
                "description": "OTP email delivery service"
            }
        }
    }
