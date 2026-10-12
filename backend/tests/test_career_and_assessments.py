import pytest
from app.models import AssessmentQuestion, UserSkillVerification

def test_career_discovery_and_comparison(client):
    # Match endpoint
    res = client.post("/api/v1/careers/match", json={
        "interests": ["Data & Analytics", "Statistics"],
        "activities": ["Building dashboards", "Querying databases"],
        "problem_solving_style": "analytical",
        "known_skills": ["SQL", "Excel", "Python"],
        "favorite_subjects": ["Mathematics", "DBMS"],
        "career_goals": "high_growth"
    })
    assert res.status_code == 200
    data = res.json()
    assert "disclaimer" in data
    assert len(data["recommended_roles"]) >= 10
    top_match = data["recommended_roles"][0]
    assert top_match["id"] in ["data-analyst", "data-scientist"]
    assert "explanation" in top_match
    assert "matching_interests" in top_match["explanation"]

    # Compare endpoint
    comp_res = client.post("/api/v1/careers/compare", json={
        "role_ids": ["data-analyst", "sde"]
    })
    assert comp_res.status_code == 200
    assert len(comp_res.json()["compared_roles"]) == 2


def test_assessment_start_and_submission(client, create_test_user, db_session):
    user, token = create_test_user("test_student", "student_assess@college.edu")
    client.cookies.set("sf_session", token)

    # 1. Start assessment (verify correct answers are omitted)
    start_res = client.get("/api/v1/assessments/start?category=Python&difficulty=Beginner")
    assert start_res.status_code == 200
    start_data = start_res.json()
    assert len(start_data["questions"]) >= 5
    for q in start_data["questions"]:
        assert "correct_answer" not in q
        assert "explanation" not in q

    # 2. Submit answers
    first_q_id = start_data["questions"][0]["id"]
    db_q = db_session.query(AssessmentQuestion).filter(AssessmentQuestion.id == first_q_id).first()

    sub_res = client.post("/api/v1/assessments/submit", json={
        "category": "Python",
        "difficulty": "Beginner",
        "time_taken_seconds": 75,
        "answers": [
            {"question_id": first_q_id, "selected_answer": db_q.correct_answer}
        ]
    })
    assert sub_res.status_code == 200
    result = sub_res.json()
    assert result["score"] >= 1.0
    assert "topic_breakdown" in result
    assert "verification_status" in result

    # 3. Verify UserSkillVerification was created with evidence (never 'certified')
    verif = db_session.query(UserSkillVerification).filter(
        UserSkillVerification.user_id == user.id,
        UserSkillVerification.skill_name == "Python"
    ).first()
    assert verif is not None
    assert verif.status in ["In progress", "Demonstrated", "Strong evidence"]
    assert "certified" not in verif.status.lower()

    # 4. Assessment History
    hist_res = client.get("/api/v1/assessments/history?category=Python")
    assert hist_res.status_code == 200
    assert hist_res.json()["total_taken"] >= 1
