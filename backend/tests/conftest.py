import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.database import Base, get_db
from app.models import User, Session as UserSession
from app.core.security import hash_password, generate_session_token
from app.main import app
from scripts.seed_db import seed_database

# Use an isolated test SQLite DB
TEST_DATABASE_URL = "sqlite:///./test_skillforage.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    # Seed career roles, questions, lessons, and jobs into test DB
    import scripts.seed_db as seeder
    seeder.SessionLocal = TestingSessionLocal
    seeder.init_db = lambda: Base.metadata.create_all(bind=test_engine)
    seeder.seed_database()
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def create_test_user(db_session):
    def _create_user(username: str, email: str, password: str = "password123", year: int = 2):
        user = User(
            username=username,
            email=email.lower().strip(),
            password_hash=hash_password(password),
            year=year,
            degree="B.Tech.",
            branch="Computer Science",
            email_verified=True,
            target_role="sde"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Create session
        token = generate_session_token()
        session_rec = UserSession(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db_session.add(session_rec)
        db_session.commit()

        return user, token
    return _create_user
