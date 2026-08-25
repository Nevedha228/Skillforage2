from ats.ats_checker import calculate_ats_score

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import tempfile
import os

from parsers.pdf_parser import extract_text_from_pdf
from parsers.resume_parser import parse_resume as parse_resume_data


app = FastAPI(title="SkillForge AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "SkillForge AI Backend Running"
    }


# MODULE 1 — Resume Parser
@app.post("/parse-resume")
async def upload_resume(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_file_path)

        resume_data = parse_resume_data(text)

        return {
            "filename": file.filename,
            "resume_data": resume_data
        }

    finally:
        os.remove(temp_file_path)


# MODULE 2 — ATS Resume Checker
@app.post("/ats-check")
async def ats_check(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_file_path)

        ats_result = calculate_ats_score(text)

        return {
            "filename": file.filename,
            "ats_analysis": ats_result
        }

    finally:
        os.remove(temp_file_path)