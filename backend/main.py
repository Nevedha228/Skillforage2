from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import tempfile
import os
import re

from parsers.pdf_parser import extract_text_from_pdf
from parsers.resume_parser import parse_resume as parse_resume_data

from ats.ats_checker import calculate_ats_score

from skill_gap.skill_gap_analyzer import analyze_skill_gap

from roadmap.roadmap_generator import generate_roadmap

# ============================================================
# MARKET INTELLIGENCE
# ============================================================

from market_engine.pipeline import run_market_pipeline

from market_engine.analytics import (
    get_top_skills,
    get_role_distribution,
    get_role_skill_analysis,
    get_salary_analysis,
    get_location_distribution,
    get_market_snapshots,
    get_market_summary,
)

from market_engine.database import (
    get_market_runs,
)


# ============================================================
# REQUEST MODELS
# ============================================================

class SkillGapRequest(BaseModel):

    resume_skills: list[str]

    education: str

    year: str

    branch: str


class RoadmapRequest(BaseModel):

    missing_skills: list[str] = []

    matched_skills: list[str] = []

    education: str = ""

    year: str = ""

    branch: str = ""

    career_status: str = ""

    interests: list[str] = []

    time_available: str = ""

    target_role: str = ""


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title="SkillForge AI",

    description=(
        "AI-powered Resume Analysis, "
        "Skill Gap Detection and "
        "Personalized Career Roadmap"
    ),

    version="3.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origin_regex=(
        r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
    ),

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

        "success": True,

        "message": "SkillForge AI Backend Running",

        "version": "3.0.0"

    }


# ============================================================
# HELPER
# ============================================================

def extract_clean_skills(skills_text):

    if not skills_text:

        return []

    skills = []

    parts = re.split(

        r"[,;|\n]",

        str(skills_text)

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

        # Remove category labels

        part = re.sub(

            r"^(programming languages|"
            r"web technologies|"
            r"databases|"
            r"tools|"
            r"concepts|"
            r"soft skills)\s*:\s*",

            "",

            part,

            flags=re.IGNORECASE

        )

        part = part.strip()

        if part:

            skills.append(part)

    # Remove duplicates

    return list(
        dict.fromkeys(skills)
    )


# ============================================================
# RESUME PARSER
# ============================================================

@app.post("/parse-resume")
async def upload_resume(

    file: UploadFile = File(...)

):

    temp_file_path = None

    try:

        # ----------------------------------------------------
        # Save uploaded PDF
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".pdf"

        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_file_path = temp_file.name

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        text = extract_text_from_pdf(

            temp_file_path

        )

        if not text.strip():

            return {

                "success": False,

                "message": (
                    "Could not extract text "
                    "from the resume."
                )

            }

        # ----------------------------------------------------
        # Parse resume
        # ----------------------------------------------------

        resume_data = parse_resume_data(

            text

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

            and os.path.exists(
                temp_file_path
            )

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

        # ----------------------------------------------------
        # Save uploaded PDF
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".pdf"

        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_file_path = temp_file.name

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        text = extract_text_from_pdf(

            temp_file_path

        )

        if not text.strip():

            return {

                "success": False,

                "message": (
                    "Could not extract text "
                    "from the resume."
                )

            }

        # ----------------------------------------------------
        # ATS analysis
        # ----------------------------------------------------

        ats_result = calculate_ats_score(

            text

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

            and os.path.exists(
                temp_file_path
            )

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

    try:

        result = analyze_skill_gap(

            resume_skills=request.resume_skills,

            education=request.education,

            year=request.year,

            branch=request.branch

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
# PERSONALIZED ROADMAP
# ============================================================

@app.post("/roadmap")
async def personalized_roadmap(

    request: RoadmapRequest

):

    try:

        result = generate_roadmap(

            missing_skills=request.missing_skills,

            matched_skills=request.matched_skills,

            education=request.education,

            year=request.year,

            branch=request.branch,

            career_status=request.career_status,

            interests=request.interests,

            time_available=request.time_available,

            target_role=request.target_role

        )

        return result

    except Exception as e:

        print(

            "ROADMAP ERROR:",

            str(e)

        )

        return {

            "success": False,

            "message": str(e),

            "roadmap_type": "",

            "student_profile": {},

            "roadmap_summary": {},

            "priority_skills": [],

            "phases": []

        }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

@app.post("/analyze")
async def analyze_resume(

    file: UploadFile = File(...),

    education: str = Form(...),

    year: str = Form(...),

    branch: str = Form(...),

    # --------------------------------------------------------
    # NEW OPTIONAL ROADMAP INPUTS
    # --------------------------------------------------------

    career_status: str = Form(""),

    interests: str = Form(""),

    time_available: str = Form(""),

    target_role: str = Form("")

):

    temp_file_path = None

    try:

        print(
            "\n========================================"
        )

        print(
            "          SKILLFORGE AI ANALYSIS"
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
            "Career Status:",
            career_status
        )

        print(
            "Interests:",
            interests
        )

        print(
            "Time Available:",
            time_available
        )

        print(
            "Target Role:",
            target_role
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
        # 2. EXTRACT TEXT
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
                    "Could not extract text from "
                    "the resume. Please upload a "
                    "text-based PDF."
                )

            }

        # ====================================================
        # 3. PARSE RESUME
        # ====================================================

        resume_data = parse_resume_data(

            text

        )

        print(
            "\nResume Parsed Successfully"
        )

        # ====================================================
        # 4. EXTRACT SKILLS
        # ====================================================

        skills_text = resume_data.get(

            "skills",

            ""

        )

        resume_skills = extract_clean_skills(

            skills_text

        )

        print(

            "Resume Skills:",

            resume_skills

        )

        # ====================================================
        # 5. ATS ANALYSIS
        # ====================================================

        ats_result = calculate_ats_score(

            text

        )

        print(

            "\nATS Result:",

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

        matched_skills = skill_gap_result.get(

            "matched_skills",

            []

        )

        missing_skills = skill_gap_result.get(

            "missing_skills",

            []

        )

        skill_gap_score = skill_gap_result.get(

            "skill_gap_score",

            0

        )

        print(

            "\nMatched Skills:",

            matched_skills

        )

        print(

            "Missing Skills:",

            missing_skills

        )

        print(

            "Skill Gap Score:",

            skill_gap_score

        )

        # ====================================================
        # 7. CLEAN INTERESTS
        # ====================================================

        interest_list = []

        if interests:

            interest_parts = re.split(

                r"[,;|\n]",

                interests

            )

            for item in interest_parts:

                item = item.strip()

                if item:

                    interest_list.append(
                        item
                    )

        # ====================================================
        # 8. GENERATE PERSONALIZED ROADMAP
        # ====================================================

        print(
            "\nGenerating Personalized Roadmap..."
        )

        roadmap_result = generate_roadmap(

            missing_skills=missing_skills,

            matched_skills=matched_skills,

            education=education,

            year=year,

            branch=branch,

            career_status=career_status,

            interests=interest_list,

            time_available=time_available,

            target_role=target_role

        )

        print(

            "Roadmap Generated:",

            roadmap_result.get(
                "success",
                False
            )

        )

        # ====================================================
        # 9. FINAL RESPONSE
        # ====================================================

        result = {

            "success": True,

            "filename": file.filename,

            # ------------------------------------------------
            # RESUME
            # ------------------------------------------------

            "resume_data": resume_data,

            "resume_skills": resume_skills,

            # ------------------------------------------------
            # ATS
            # ------------------------------------------------

            "ats_analysis": ats_result,

            "ats_score": ats_result.get(

                "ats_score",

                0

            ),

            # ------------------------------------------------
            # SKILL GAP
            # ------------------------------------------------

            "skill_gap": skill_gap_result,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "skill_gap_score": skill_gap_score,

            # ------------------------------------------------
            # ROADMAP
            # ------------------------------------------------

            "roadmap": roadmap_result

        }

        # ====================================================
        # 10. PRINT FINAL RESULT
        # ====================================================

        print(
            "\n========================================"
        )

        print(
            "          FINAL ANALYSIS RESULT"
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

            "Roadmap Type:",

            roadmap_result.get(
                "roadmap_type",
                ""
            )

        )

        print(

            "Priority Skills:",

            roadmap_result.get(
                "priority_skills",
                []
            )

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

            "skill_gap_score": 0,

            "roadmap": {

                "success": False,

                "roadmap_type": "",

                "student_profile": {},

                "roadmap_summary": {},

                "priority_skills": [],

                "phases": []

            }

        }

    finally:

        # ====================================================
        # DELETE TEMP FILE
        # ====================================================

        if (

            temp_file_path

            and os.path.exists(
                temp_file_path
            )

        ):

            os.remove(
                temp_file_path
            )
            # ============================================================
# MARKET INTELLIGENCE API
# ============================================================


# ============================================================
# MARKET SUMMARY
# ============================================================

@app.get("/market/summary")
async def market_summary(
    role: str = ""
):
    try:

        result = get_market_summary(
            role=role
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        print(
            "MARKET SUMMARY ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# TOP MARKET SKILLS
# ============================================================

@app.get("/market/skills")
async def market_skills(
    role: str = "",
    limit: int = 10
):
    try:

        result = get_top_skills(
            limit=limit,
            normalized_role=role
        )

        return {
            "success": True,
            "role": role,
            "skills": result
        }

    except Exception as e:

        print(
            "MARKET SKILLS ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "skills": []
        }


# ============================================================
# ROLE DISTRIBUTION
# ============================================================

@app.get("/market/roles")
async def market_roles():

    try:

        result = get_role_distribution()

        return {
            "success": True,
            "roles": result
        }

    except Exception as e:

        print(
            "MARKET ROLES ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "roles": []
        }


# ============================================================
# ROLE-SPECIFIC SKILL ANALYSIS
# ============================================================

@app.get("/market/role-skills")
async def market_role_skills(
    role: str,
    limit: int = 10
):
    try:

        result = get_role_skill_analysis(
            role=role,
            limit=limit
        )

        return {
            "success": True,
            "role": role,
            "skills": result
        }

    except Exception as e:

        print(
            "ROLE SKILL ANALYSIS ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "skills": []
        }


# ============================================================
# SALARY ANALYSIS
# ============================================================

@app.get("/market/salary")
async def market_salary(
    role: str = ""
):
    try:

        result = get_salary_analysis(
            normalized_role=role
        )

        return {
            "success": True,
            "role": role,
            "salary": result
        }

    except Exception as e:

        print(
            "MARKET SALARY ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "salary": {}
        }


# ============================================================
# LOCATION DISTRIBUTION
# ============================================================

@app.get("/market/locations")
async def market_locations(
    limit: int = 10
):
    try:

        result = get_location_distribution(
            limit=limit
        )

        return {
            "success": True,
            "locations": result
        }

    except Exception as e:

        print(
            "MARKET LOCATIONS ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "locations": []
        }


# ============================================================
# MARKET SNAPSHOTS
# ============================================================

@app.get("/market/snapshots")
async def market_snapshots(
    role: str = "",
    skill: str = ""
):
    try:

        result = get_market_snapshots(
            role=role,
            skill=skill
        )

        return {
            "success": True,
            "snapshots": result
        }

    except Exception as e:

        print(
            "MARKET SNAPSHOT ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "snapshots": []
        }


# ============================================================
# MARKET RUN HISTORY
# ============================================================

@app.get("/market/runs")
async def market_runs():

    try:

        result = get_market_runs()

        return {
            "success": True,
            "runs": result
        }

    except Exception as e:

        print(
            "MARKET RUNS ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "runs": []
        }


# ============================================================
# RUN MARKET INTELLIGENCE PIPELINE
# ============================================================

@app.post("/market/run")
async def run_market_analysis(
    role: str = "data analyst",
    country: str = "in",
    pages: int = 3,
    results_per_page: int = 20,
    location: str = ""
):
    try:

        result = run_market_pipeline(

            role=role,

            country=country,

            pages=pages,

            results_per_page=results_per_page,

            location=location
        )

        return {
            "success": True,
            "market_analysis": result
        }

    except Exception as e:

        print(
            "MARKET PIPELINE ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e)
        }
    # ============================================================
# AUTOMATIC MARKET ANALYSIS
# ============================================================

from fastapi import Query


@app.post("/market/analyze")
def analyze_market(
    role: str = Query(..., description="Target career role"),
    country: str = Query("in", description="Adzuna country code"),
    pages: int = Query(1, ge=1, le=5),
    results_per_page: int = Query(20, ge=10, le=50),
    location: str = Query("", description="Optional job location"),
):
    """
    Automatically collect fresh jobs for the selected role,
    process them, extract skills, store them, and return
    role-specific market intelligence.
    """

    try:
        # ----------------------------------------------------
        # Validate role
        # ----------------------------------------------------
        role = role.strip()

        if not role:
            return {
                "success": False,
                "message": "Please provide a target role."
            }

        # ----------------------------------------------------
        # Run fresh market collection
        # ----------------------------------------------------
        market_analysis = run_market_pipeline(
            role=role,
            country=country,
            pages=pages,
            results_per_page=results_per_page,
            location=location,
        )

        # ----------------------------------------------------
        # Read role-specific analytics
        # ----------------------------------------------------
        market_summary = get_market_summary(role=role)

        # ----------------------------------------------------
        # Return combined result
        # ----------------------------------------------------
        return {
            "success": True,
            "market_analysis": market_analysis,
            "data": market_summary,
        }

    except Exception as error:
        print("MARKET ANALYSIS ERROR:", error)

        return {
            "success": False,
            "message": str(error),
        }