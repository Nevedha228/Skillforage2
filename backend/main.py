from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import tempfile
import os
import re

from parsers.pdf_parser import extract_text_from_pdf
from parsers.resume_parser import parse_resume as parse_resume_data
from skill_gap.skill_gap_analyzer import analyze_skill_gap
from ats.ats_checker import calculate_ats_score


# ============================================================
# REQUEST MODEL
# ============================================================

class SkillGapRequest(BaseModel):
    resume_skills: list[str]
    education: str
    year: str
    branch: str


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="SkillForge AI",
    description="AI-powered Resume Skill Gap Analyzer",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "SkillForge AI Backend Running"
    }


# ============================================================
# HELPER
# ============================================================

def extract_clean_skills(skills_text):

    if not skills_text:
        return []

    skills = []

    # Split skills by comma, semicolon, pipe or newline
    parts = re.split(
        r"[,;|\n]",
        skills_text
    )

    for part in parts:

        part = part.strip()

        if not part:
            continue

        # Remove bullets
        part = re.sub(
            r"^[•\-*]\s*",
            "",
            part
        )

        # Remove category names
        part = re.sub(
            r"^(programming languages|web technologies|databases|tools|concepts|soft skills)\s*:\s*",
            "",
            part,
            flags=re.IGNORECASE
        )

        part = part.strip()

        if part:
            skills.append(part)

    # Remove duplicates
    return list(dict.fromkeys(skills))


# ============================================================
# RESUME PARSER
# ============================================================

@app.post("/parse-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    temp_file_path = None

    try:

        # --------------------------------------------
        # Save uploaded file
        # --------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_file_path = temp_file.name

        # --------------------------------------------
        # Extract PDF text
        # --------------------------------------------

        text = extract_text_from_pdf(
            temp_file_path
        )

        print("\n========== RESUME PARSER ==========")

        print(
            "Filename:",
            file.filename
        )

        print(
            "Extracted text length:",
            len(text)
        )

        # --------------------------------------------
        # Parse resume
        # --------------------------------------------

        resume_data = parse_resume_data(
            text
        )

        print(
            "Resume Data:",
            resume_data
        )

        print(
            "===================================\n"
        )

        return {

            "success": True,

            "filename": file.filename,

            "resume_data": resume_data,

            "text_length": len(text)
        }

    except Exception as e:

        print(
            "RESUME PARSER ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message": str(e)
        }

    finally:

        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):

            os.remove(
                temp_file_path
            )


# ============================================================
# ATS CHECKER
# ============================================================

@app.post("/ats-check")
async def ats_check(
    file: UploadFile = File(...)
):

    temp_file_path = None

    try:

        # --------------------------------------------
        # Save uploaded file
        # --------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_file_path = temp_file.name

        # --------------------------------------------
        # Extract text
        # --------------------------------------------

        text = extract_text_from_pdf(
            temp_file_path
        )

        # --------------------------------------------
        # ATS analysis
        # --------------------------------------------

        ats_result = calculate_ats_score(
            text
        )

        print("\n========== ATS CHECK ==========")

        print(
            "Filename:",
            file.filename
        )

        print(
            "ATS Result:",
            ats_result
        )

        print(
            "===============================\n"
        )

        return {

            "success": True,

            "filename": file.filename,

            "ats_analysis": ats_result
        }

    except Exception as e:

        print(
            "ATS ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message": str(e)
        }

    finally:

        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):

            os.remove(
                temp_file_path
            )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

@app.post("/skill-gap")
async def skill_gap_analysis(
    request: SkillGapRequest
):

    print(
        "\n========== SKILL GAP REQUEST =========="
    )

    print(
        "Education:",
        request.education
    )

    print(
        "Year:",
        request.year
    )

    print(
        "Branch:",
        request.branch
    )

    print(
        "Resume Skills:",
        request.resume_skills
    )

    try:

        result = analyze_skill_gap(

            resume_skills=request.resume_skills,

            education=request.education,

            year=request.year,

            branch=request.branch
        )

        print(
            "Skill Gap Result:",
            result
        )

        print(
            "=======================================\n"
        )

        return result

    except Exception as e:

        print(
            "SKILL GAP ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message": str(e),

            "matched_skills": [],

            "missing_skills": [],

            "skill_gap_score": 0
        }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================
#
# This is the main endpoint your React Analyze button
# should eventually call.
#
# It performs:
#
# PDF extraction
#       ↓
# Resume parsing
#       ↓
# Skill extraction
#       ↓
# ATS analysis
#       ↓
# Skill gap analysis
#       ↓
# One final JSON response
#
# ============================================================

@app.post("/analyze")
async def analyze_resume(

    file: UploadFile = File(...),

    education: str = Form(...),

    year: str = Form(...),

    branch: str = Form(...)
):

    temp_file_path = None

    try:

        print(
            "\n\n========================================"
        )

        print(
            "       SKILLFORGE AI ANALYSIS"
        )

        print(
            "========================================"
        )

        print(
            "Education:",
            education
        )

        print(
            "Year:",
            year
        )

        print(
            "Branch:",
            branch
        )

        print(
            "Filename:",
            file.filename
        )

        # ====================================================
        # 1. SAVE RESUME
        # ====================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_file_path = temp_file.name

        # ====================================================
        # 2. EXTRACT RESUME TEXT
        # ====================================================

        text = extract_text_from_pdf(
            temp_file_path
        )

        print(
            "\nExtracted text characters:",
            len(text)
        )

        if not text.strip():

            return {

                "success": False,

                "message": (
                    "Could not extract text from the resume. "
                    "Please upload a text-based PDF."
                )
            }

        # ====================================================
        # 3. PARSE RESUME
        # ====================================================

        resume_data = parse_resume_data(
            text
        )

        print(
            "\nParsed Resume:"
        )

        print(
            resume_data
        )

        # ====================================================
        # 4. EXTRACT CLEAN SKILLS
        # ====================================================

        skills_text = resume_data.get(
            "skills",
            ""
        )

        resume_skills = extract_clean_skills(
            skills_text
        )

        print(
            "\nClean Resume Skills:"
        )

        print(
            resume_skills
        )

        # ====================================================
        # 5. ATS ANALYSIS
        # ====================================================

        ats_result = calculate_ats_score(
            text
        )

        print(
            "\nATS Result:"
        )

        print(
            ats_result
        )

        # ====================================================
        # 6. SKILL GAP ANALYSIS
        # ====================================================

        skill_gap_result = analyze_skill_gap(

            resume_skills=resume_skills,

            education=education,

            year=year,

            branch=branch
        )

        print(
            "\nSkill Gap Result:"
        )

        print(
            skill_gap_result
        )

        # ====================================================
        # 7. FINAL RESPONSE
        # ====================================================

        result = {

            "success": True,

            "filename": file.filename,

            # --------------------------------------------
            # Resume
            # --------------------------------------------

            "resume_data": resume_data,

            "resume_skills": resume_skills,

            # --------------------------------------------
            # ATS
            # --------------------------------------------

            "ats_analysis": ats_result,

            # --------------------------------------------
            # Skill Gap
            # --------------------------------------------

            "skill_gap": skill_gap_result,

            # --------------------------------------------
            # Easy frontend fields
            # --------------------------------------------

            "ats_score": ats_result.get(
                "ats_score",
                0
            ),

            "matched_skills": skill_gap_result.get(
                "matched_skills",
                []
            ),

            "missing_skills": skill_gap_result.get(
                "missing_skills",
                []
            ),

            "skill_gap_score": skill_gap_result.get(
                "skill_gap_score",
                0
            )
        }

        print(
            "\n========================================"
        )

        print(
            "         FINAL ANALYSIS RESULT"
        )

        print(
            "========================================"
        )

        print(
            "ATS Score:",
            result["ats_score"]
        )

        print(
            "Matched Skills:",
            result["matched_skills"]
        )

        print(
            "Missing Skills:",
            result["missing_skills"]
        )

        print(
            "Skill Gap Score:",
            result["skill_gap_score"]
        )

        print(
            "========================================\n"
        )

        return result

    except Exception as e:

        print(
            "\n========================================"
        )

        print(
            "ANALYSIS ERROR:"
        )

        print(
            str(e)
        )

        print(
            "========================================\n"
        )

        return {

            "success": False,

            "message": str(e),

            "ats_score": 0,

            "matched_skills": [],

            "missing_skills": [],

            "skill_gap_score": 0
        }

    finally:

        # ====================================================
        # DELETE TEMP FILE
        # ====================================================

        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):

            os.remove(
                temp_file_path
            )