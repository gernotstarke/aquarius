import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Disable app authentication for tests
os.environ["ENABLE_APP_AUTH"] = "false"

# Add the backend directory to sys.path so 'app' module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from app.main import app
from app import models, auth

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create a test client with a DB dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Do not close the session here; it's managed by the db fixture
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def admin_token_headers(client, db):
    """Create an admin user and return auth headers."""
    # Create admin user
    from app.auth import get_password_hash
    password = "admin_test_password"
    admin_user = models.User(
        username="admin_test",
        hashed_password=get_password_hash(password),
        role="ADMIN",  # Changed from ROOT to ADMIN for admin endpoints
        is_active=True,
        is_app_user=False,
        can_read_all=True,
        can_write_all=True,
    )
    db.add(admin_user)
    db.commit()

    # Login to get token
    login_data = {
        "username": "admin_test",
        "password": password
    }
    response = client.post("/api/auth/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def app_token_headers(client, db):
    """Create an app user with read/write permissions and return auth headers."""
    from app.auth import get_password_hash, create_access_token

    app_user = models.User(
        username="app_test_user",
        full_name="Test App User",
        hashed_password=get_password_hash("app-test-password"),
        role="VERWALTUNG",
        is_active=True,
        is_app_user=True,
        can_read_all=True,
        can_write_all=True,
    )
    db.add(app_user)
    db.commit()

    token = create_access_token({"sub": app_user.username})
    return {"Authorization": f"Bearer {token}"}

