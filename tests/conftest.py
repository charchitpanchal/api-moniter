import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:chinu123@localhost:5432/api_monitor_test",
)

from app.main import app
from app.db.database import Base, get_db
from app.core.config import settings

TEST_DATABASE_URL = settings.database_url

engine = create_engine(TEST_DATABASE_URL, future=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates all tables fresh before each test, drops them after.
    Ensures complete test isolation — no leftover data between tests.
    """
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI TestClient with the DB dependency overridden to use
    the test session instead of the real database.
    """
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
def registered_user(client):
    """Registers a test user and returns their credentials."""
    payload = {"name": "Test User", "email": "testuser@example.com", "password": "testpass123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    return payload


@pytest.fixture
def auth_token(client, registered_user):
    """Logs in the registered test user and returns a valid JWT."""
    response = client.post(
        "/api/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}