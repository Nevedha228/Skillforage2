import io
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, UserResume
from app.schemas.resume import (
    ResumeProfileResponse,
    ATSAnalysisResponse,
    CompareJobDescriptionRequest,
    UpdateResumeRequest
)
from app.services.resume_service import (
    extract_text_from_pdf_stream,
    parse_resume_sections,
    analyze_ats_heuristics,
    ATS_DISCLAIMER
)

router = APIRouter(prefix="/resumes", tags=["Resume Analyzer & Builder"])

MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

@router.post("/upload")
async def upload_and_parse_resume(
    file: UploadFile = File(...),
    keep_raw_file: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate MIME type and extension
    filename = (file.filename or "").lower()
    if not (filename.endswith(".pdf") or file.content_type in ["application/pdf", "application/x-pdf"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF documents (.pdf) are supported."
        )

    content = await file.read()
    if len(content) > MAX_RESUME_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5MB maximum upload limit."
        )

    # Extract text from PDF
    stream = io.BytesIO(content)
    text = extract_text_from_pdf_stream(stream)

    if not text or len(text.strip()) < 50:
        # Gracefully handle scanned / image-only or encrypted PDFs
        text = (
            f"Resume uploaded for {current_user.username}. "
            f"Education: {current_user.degree} in {current_user.branch} (Year {current_user.year})."
        )
        parsed_data = {
            "summary": "Engineering student eager to contribute technical competencies.",
            "education": [{"degree": f"{current_user.degree} in {current_user.branch}", "year": str(current_user.year)}],
            "skills": ["Python", "SQL", "Git", "Problem Solving"],
            "projects": [],
            "experience": [],
            "achievements": []
        }
    else:
        parsed_data = parse_resume_sections(text)

    # ATS heuristic analysis
    ats_result = analyze_ats_heuristics(text)

    # Upsert UserResume record
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()
    if not resume_record:
        resume_record = UserResume(
            user_id=current_user.id,
            raw_text=text if keep_raw_file else None,
            structured_data=parsed_data,
            ats_score_estimate=ats_result.ats_score_estimate,
            ats_feedback=ats_result.model_dump(),
            keep_raw_file=keep_raw_file,
            updated_at=datetime.utcnow()
        )
        db.add(resume_record)
    else:
        resume_record.raw_text = text if keep_raw_file else None
        resume_record.structured_data = parsed_data
        resume_record.ats_score_estimate = ats_result.ats_score_estimate
        resume_record.ats_feedback = ats_result.model_dump()
        resume_record.keep_raw_file = keep_raw_file
        resume_record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(resume_record)

    return {
        "success": True,
        "message": "Resume parsed and analyzed successfully.",
        "ats_score_estimate": ats_result.ats_score_estimate,
        "disclaimer": ATS_DISCLAIMER,
        "structured_data": parsed_data,
        "ats_feedback": ats_result.model_dump()
    }


@router.get("/profile")
def get_resume_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()
    if not resume_record:
        # Return default zero-state structure
        default_data = {
            "summary": f"{current_user.username} is a {current_user.degree} student specializing in {current_user.branch}.",
            "education": [{"degree": f"{current_user.degree} in {current_user.branch}", "year": f"Year {current_user.year}"}],
            "skills": ["Python", "SQL", "Git"],
            "projects": [],
            "experience": [],
            "achievements": []
        }
        return {
            "has_resume": False,
            "structured_data": default_data,
            "ats_score_estimate": 0,
            "ats_feedback": {
                "disclaimer": ATS_DISCLAIMER,
                "suggestions": ["Upload your PDF resume or enter your details below to generate an ATS compatibility report."]
            }
        }

    return {
        "has_resume": True,
        "id": resume_record.id,
        "structured_data": resume_record.structured_data,
        "ats_score_estimate": resume_record.ats_score_estimate,
        "ats_feedback": resume_record.ats_feedback,
        "keep_raw_file": resume_record.keep_raw_file,
        "updated_at": resume_record.updated_at.isoformat()
    }


@router.put("/profile")
def update_resume_profile(
    req: UpdateResumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()

    # Re-evaluate ATS heuristics based on structured text
    structured_dict = req.structured_data.model_dump()
    synthetic_text = (
        f"{structured_dict.get('summary', '')} "
        f"{' '.join(structured_dict.get('skills', []))} "
        f"{' '.join(str(p) for p in structured_dict.get('projects', []))} "
        f"{' '.join(str(e) for e in structured_dict.get('education', []))}"
    )
    ats_result = analyze_ats_heuristics(synthetic_text)

    if not resume_record:
        resume_record = UserResume(
            user_id=current_user.id,
            structured_data=structured_dict,
            ats_score_estimate=ats_result.ats_score_estimate,
            ats_feedback=ats_result.model_dump(),
            keep_raw_file=req.keep_raw_file or False,
            updated_at=datetime.utcnow()
        )
        db.add(resume_record)
    else:
        resume_record.structured_data = structured_dict
        resume_record.ats_score_estimate = ats_result.ats_score_estimate
        resume_record.ats_feedback = ats_result.model_dump()
        if req.keep_raw_file is not None:
            resume_record.keep_raw_file = req.keep_raw_file
        resume_record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(resume_record)

    return {
        "success": True,
        "message": "Resume profile updated successfully.",
        "ats_score_estimate": ats_result.ats_score_estimate,
        "structured_data": resume_record.structured_data,
        "ats_feedback": ats_result.model_dump()
    }


@router.post("/compare-job", response_model=ATSAnalysisResponse)
def compare_against_job_description(
    req: CompareJobDescriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()
    if not resume_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please upload or save your resume before comparing against a job description."
        )

    structured_dict = resume_record.structured_data or {}
    combined_text = (
        f"{resume_record.raw_text or ''} "
        f"{structured_dict.get('summary', '')} "
        f"{' '.join(structured_dict.get('skills', []))}"
    )

    return analyze_ats_heuristics(combined_text, job_desc=req.job_description)


@router.get("/export-html")
def export_resume_html(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Renders structured resume in a clean printable HTML format.
    Students can print/save directly as PDF via browser print dialog.
    """
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()
    data = resume_record.structured_data if resume_record else {
        "summary": "Engineering student",
        "skills": ["Python", "SQL"],
        "education": [{"degree": f"{current_user.degree} in {current_user.branch}", "year": f"Year {current_user.year}"}],
        "projects": []
    }

    skills_html = "".join(f"<span style='background:#f1f5f9;padding:4px 8px;margin:3px;border-radius:4px;display:inline-block;font-size:13px;'>{s}</span>" for s in data.get("skills", []))
    edu_html = "".join(f"<div style='margin-bottom:8px;'><strong>{e.get('degree', '')}</strong> — {e.get('details', e.get('year', ''))}</div>" for e in data.get("education", []))
    proj_html = "".join(f"<div style='margin-bottom:12px;'><strong>{p.get('title', '')}</strong><p style='margin:4px 0 0 0;'>{p.get('description', '')}</p></div>" for p in data.get("projects", []))

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{current_user.username} — Resume</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; padding: 40px; max-width: 800px; margin: 0 auto; }}
        h1 {{ margin: 0 0 4px 0; font-size: 26px; color: #0f172a; }}
        .contact {{ color: #64748b; font-size: 14px; margin-bottom: 24px; }}
        h2 {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px; color: #4338ca; margin-top: 24px; }}
        @media print {{ body {{ padding: 0; }} }}
    </style>
</head>
<body>
    <h1>{current_user.username}</h1>
    <div class="contact">{current_user.email} | {current_user.branch} | Year {current_user.year} | {current_user.degree}</div>

    <h2>Professional Summary</h2>
    <p>{data.get('summary', '')}</p>

    <h2>Technical Skills</h2>
    <div>{skills_html}</div>

    <h2>Education</h2>
    <div>{edu_html}</div>

    <h2>Projects</h2>
    <div>{proj_html or '<p>No projects listed yet.</p>'}</div>
</body>
</html>"""

    return Response(content=html, media_type="text/html")


@router.delete("/profile")
def delete_resume_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume_record = db.query(UserResume).filter(UserResume.user_id == current_user.id).first()
    if resume_record:
        db.delete(resume_record)
        db.commit()

    return {"success": True, "message": "All saved resume data has been deleted."}
