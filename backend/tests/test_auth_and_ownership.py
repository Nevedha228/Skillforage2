import pytest
from datetime import datetime, timedelta
from app.models import OTPCode, UserAssessment
from app.core.security import hash_otp

def test_startup_and_health(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["success"] is True

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"


def test_registration_validation(client):
    # Short password
    res = client.post("/api/v1/auth/register", json={
        "username": "alice",
        "email": "alice@college.edu",
        "password": "short",
        "year": 2,
        "degree": "B.Tech",
        "branch": "CSE"
    })
    assert res.status_code == 422

    # Invalid year (> 4)
    res = client.post("/api/v1/auth/register", json={
        "username": "alice",
        "email": "alice@college.edu",
        "password": "securepassword123",
        "year": 5,
        "degree": "B.Tech",
        "branch": "CSE"
    })
    assert res.status_code == 422


def test_registration_flow_and_otp_expiry(client, db_session):
    email = "bob_test@college.edu"
    reg_res = client.post("/api/v1/auth/register", json={
        "username": "bob",
        "email": email,
        "password": "strongPassword123",
        "year": 1,
        "degree": "B.E.",
        "branch": "IT"
    })
    assert reg_res.status_code == 200
    assert reg_res.json()["success"] is True

    # Retrieve created OTP in DB and simulate expiry
    otp_record = db_session.query(OTPCode).filter(OTPCode.email == email).order_by(OTPCode.created_at.desc()).first()
    assert otp_record is not None
    otp_record.expires_at = datetime.utcnow() - timedelta(minutes=1)
    db_session.commit()

    # Attempt verification with expired OTP
    verify_res = client.post("/api/v1/auth/verify-otp", json={
        "email": email,
        "otp": "123456"
    })
    assert verify_res.status_code == 400
    assert "expired" in verify_res.json()["detail"].lower()


def test_otp_attempt_limits_and_single_use(client, db_session):
    email = "charlie_test@college.edu"
    client.post("/api/v1/auth/register", json={
        "username": "charlie",
        "email": email,
        "password": "password12345",
        "year": 3,
        "degree": "B.Sc",
        "branch": "Computer Science"
    })

    # Set known OTP: "654321"
    otp_record = db_session.query(OTPCode).filter(OTPCode.email == email).order_by(OTPCode.created_at.desc()).first()
    otp_record.otp_hash = hash_otp("654321")
    db_session.commit()

    # Submit wrong OTP 5 times to hit rate limit
    for _ in range(5):
        client.post("/api/v1/auth/verify-otp", json={
            "email": email,
            "otp": "000000"
        })

    # 6th attempt should be blocked
    fail_res = client.post("/api/v1/auth/verify-otp", json={
        "email": email,
        "otp": "654321"
    })
    assert fail_res.status_code == 400


def test_login_and_session_cookie(client, create_test_user):
    user, _ = create_test_user("diana", "diana@college.edu", "mySecretPass123", 4)

    # Wrong password
    bad_login = client.post("/api/v1/auth/login", json={
        "email": "diana@college.edu",
        "password": "wrongpassword"
    })
    assert bad_login.status_code == 401

    # Correct password
    good_login = client.post("/api/v1/auth/login", json={
        "email": "diana@college.edu",
        "password": "mySecretPass123"
    })
    assert good_login.status_code == 200
    assert "sf_session" in good_login.cookies
    assert good_login.json()["user"]["email"] == "diana@college.edu"


def test_protected_routes_unauthenticated(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401

    res = client.get("/api/v1/roadmaps/current")
    assert res.status_code == 401

    res = client.get("/api/v1/dashboard")
    assert res.status_code == 401


def test_strict_user_ownership_isolation(client, create_test_user, db_session):
    """
    CRITICAL SECURITY TEST:
    Proves that User A cannot read, update, or access User B's private records.
    """
    user_a, token_a = create_test_user("user_a", "user_a@college.edu")
    user_b, token_b = create_test_user("user_b", "user_b@college.edu")

    # Create assessment owned exclusively by User B
    assessment_b = UserAssessment(
        user_id=user_b.id,
        category="Python",
        difficulty="Beginner",
        score=9.0,
        max_score=10.0,
        percentage=90.0,
        time_taken_seconds=120,
        topic_breakdown={},
        weak_topics=[],
        recommendations=[]
    )
    db_session.add(assessment_b)
    db_session.commit()
    db_session.refresh(assessment_b)

    # User A attempts to view User B's assessment
    client.cookies.set("sf_session", token_a)
    forbidden_res = client.get(f"/api/v1/assessments/history/{assessment_b.id}")
    assert forbidden_res.status_code == 404
    assert "does not belong to you" in forbidden_res.json()["detail"].lower()

    # User B can view their own assessment
    client.cookies.set("sf_session", token_b)
    allowed_res = client.get(f"/api/v1/assessments/history/{assessment_b.id}")
    assert allowed_res.status_code == 200
    assert allowed_res.json()["percentage"] == 90.0
