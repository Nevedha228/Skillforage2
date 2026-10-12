import pytest
from app.models import UserLearningProgress, UserXPLog

def test_year_aware_roadmap_and_rescheduling(client, create_test_user):
    user, token = create_test_user("roadmap_user", "road_user@college.edu", year=1)
    client.cookies.set("sf_session", token)

    # 1. Generate Roadmap for Year 1 student
    res = client.post("/api/v1/roadmaps/generate", json={
        "target_role": "sde",
        "weekly_hours": 10.0
    })
    assert res.status_code == 200
    roadmap_data = res.json()
    assert "Foundations" in roadmap_data["year_emphasis"]
    assert len(roadmap_data["phases"]) == 4

    # 2. Complete a task
    first_task_id = roadmap_data["phases"][0]["tasks"][0]["id"]
    complete_res = client.post("/api/v1/roadmaps/complete-task", json={
        "task_id": first_task_id
    })
    assert complete_res.status_code == 200
    assert complete_res.json()["completed_tasks_count"] == 1
    assert complete_res.json()["progress_percentage"] > 0

    # 3. Reschedule non-judgmentally
    resched_res = client.post("/api/v1/roadmaps/reschedule", json={
        "reason": "Midterm exams",
        "adjusted_weekly_hours": 6.0
    })
    assert resched_res.status_code == 200
    assert resched_res.json()["weekly_hours"] == 6.0
    assert resched_res.json()["version"] >= 2


def test_learning_hub_quiz_gating_and_idempotent_xp(client, create_test_user, db_session):
    user, token = create_test_user("learner_user", "learner@college.edu")
    client.cookies.set("sf_session", token)

    # 1. List lessons
    lessons_res = client.get("/api/v1/learning/lessons?category=Python")
    assert lessons_res.status_code == 200
    lessons = lessons_res.json()
    assert len(lessons) >= 3
    first_lesson_id = lessons[0]["id"]

    # 2. View lesson detail (MUST NOT mark as complete)
    detail_res = client.get(f"/api/v1/learning/lessons/{first_lesson_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["is_completed"] is False
    assert "content_markdown" in detail_res.json()

    # 3. Submit correct quiz answer to complete lesson
    # Retrieve correct answer directly from DB
    from app.models import Lesson
    db_lesson = db_session.query(Lesson).filter(Lesson.id == first_lesson_id).first()
    correct_ans = db_lesson.quiz.get("correct_answer")

    quiz_res = client.post(f"/api/v1/learning/lessons/{first_lesson_id}/submit-quiz", json={
        "selected_answer": correct_ans,
        "time_spent_minutes": 15
    })
    assert quiz_res.status_code == 200
    assert quiz_res.json()["is_correct"] is True
    assert quiz_res.json()["lesson_completed"] is True
    assert quiz_res.json()["xp_awarded"] > 0

    # 4. Duplicate prevention test: Submitting quiz again should NOT award duplicate XP
    quiz_res_again = client.post(f"/api/v1/learning/lessons/{first_lesson_id}/submit-quiz", json={
        "selected_answer": correct_ans,
        "time_spent_minutes": 15
    })
    assert quiz_res_again.status_code == 200
    assert quiz_res_again.json()["xp_awarded"] == 0

    # Verify XP logs count in DB
    ref_id = f"lesson_{first_lesson_id}"
    xp_entries = db_session.query(UserXPLog).filter(
        UserXPLog.user_id == user.id,
        UserXPLog.action_type == "lesson_complete",
        UserXPLog.reference_id == ref_id
    ).all()
    assert len(xp_entries) == 1
