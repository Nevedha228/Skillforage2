import io
import pytest
from app.models import UserResume

def test_resume_upload_and_ats_analysis(client, create_test_user):
    user, token = create_test_user("resume_user", "resume_user@college.edu")
    client.cookies.set("sf_session", token)

    # 1. Non-PDF rejected
    bad_file = io.BytesIO(b"Hello world text file")
    bad_res = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.txt", bad_file, "text/plain")}
    )
    assert bad_res.status_code == 400

    # 2. Valid PDF stream simulation
    pdf_content = b"%PDF-1.4 sample content with Python, SQL, React, and Fastapi keywords"
    good_file = io.BytesIO(pdf_content)
    upload_res = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", good_file, "application/pdf")},
        data={"keep_raw_file": "false"}
    )
    assert upload_res.status_code == 200
    res_data = upload_res.json()
    assert res_data["success"] is True
    assert "ats_score_estimate" in res_data
    assert "disclaimer" in res_data

    # 3. View resume profile
    prof_res = client.get("/api/v1/resumes/profile")
    assert prof_res.status_code == 200
    assert prof_res.json()["has_resume"] is True

    # 4. Export HTML
    export_res = client.get("/api/v1/resumes/export-html")
    assert export_res.status_code == 200
    assert "text/html" in export_res.headers["content-type"]
    assert "resume_user" in export_res.text


def test_mock_interview_rubric_evaluation(client, create_test_user):
    user, token = create_test_user("interview_user", "interview_user@college.edu")
    client.cookies.set("sf_session", token)

    # 1. Start interview session
    start_res = client.post("/api/v1/interviews/start", json={
        "target_role": "sde",
        "interview_type": "technical",
        "difficulty": "Intermediate"
    })
    assert start_res.status_code == 200
    start_data = start_res.json()
    assert len(start_data["questions"]) >= 2
    assert "disclaimer" in start_data

    # 2. Submit answers
    submit_res = client.post("/api/v1/interviews/submit", json={
        "target_role": "sde",
        "interview_type": "technical",
        "difficulty": "Intermediate",
        "time_taken_seconds": 240,
        "answers": [
            {
                "question_id": 1,
                "question": "Explain process vs thread",
                "answer_text": "Processes are isolated instances with their own virtual memory address space. Threads exist within a process and share the same heap memory space, communicating via shared state and synchronization mutexes to avoid race conditions. Time complexity is O(1) for thread switching compared to process context switches."
            }
        ]
    })
    assert submit_res.status_code == 200
    res_data = submit_res.json()
    assert "rubric_scores" in res_data
    assert res_data["rubric_scores"]["correctness"] > 50
    assert "feedback" in res_data
    # Honest fallback status
    assert res_data["feedback"]["llm_status"] in ["heuristic_rubric_fallback", "ai_evaluated"]


def test_what_if_and_emergency_sprint(client, create_test_user):
    user, token = create_test_user("simulator_user", "sim_user@college.edu")
    client.cookies.set("sf_session", token)

    # What-If simulator
    sim_res = client.post("/api/v1/what-if/simulate", json={
        "scenario_a": {
            "name": "Intensive Pacing",
            "daily_hours": 3.0,
            "additional_skills": ["SQL", "FastAPI"],
            "projects_to_complete": 2,
            "months_until_placement": 4
        },
        "scenario_b": {
            "name": "Steady Pacing",
            "daily_hours": 1.0,
            "additional_skills": ["SQL"],
            "projects_to_complete": 1,
            "months_until_placement": 4
        }
    })
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert "disclaimer" in sim_data
    assert sim_data["scenario_a_result"]["projected_readiness_pct"] > sim_data["scenario_b_result"]["projected_readiness_pct"]

    # Emergency Sprint
    sprint_res = client.post("/api/v1/sprint/plan", json={
        "target_role": "sde",
        "days_left": 14,
        "hours_per_day": 3.5,
        "current_level": "Developing",
        "interview_type": "technical"
    })
    assert sprint_res.status_code == 200
    sprint_data = sprint_res.json()
    assert sprint_data["duration_days"] == 14
    assert len(sprint_data["daily_schedule"]) == 14


def test_dashboard_persisted_metrics_and_zero_state(client, create_test_user):
    user, token = create_test_user("fresh_user", "fresh@college.edu")
    client.cookies.set("sf_session", token)

    dash_res = client.get("/api/v1/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    # Zero state should be true for fresh user
    assert dash_data["is_empty_state"] is True
    assert dash_data["total_assessments_taken"] == 0
    assert len(dash_data["onboarding_checklist"]) >= 4
