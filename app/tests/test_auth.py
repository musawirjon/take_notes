import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.auth.security import get_password_hash

client = TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_user(db: Session, test_user_data):
    user = User(
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        full_name=test_user_data["full_name"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_register_success(client, test_user_data):
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data

def test_register_existing_email(client, test_user, test_user_data):
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client, test_user, test_user_data):
    response = client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_email(client, test_user_data):
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": test_user_data["password"]
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_invalid_password(client, test_user, test_user_data):
    response = client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_protected_job_endpoints(auth_client, client):
    # Test unauthorized access
    response = client.get("/api/jobs/")
    assert response.status_code == 401

    # Test authorized access
    response = auth_client.get("/api/jobs/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_job_creation_with_auth(auth_client, db):
    response = auth_client.post(
        "/api/jobs/",
        json={
            "queue": "test",
            "payload": {"test": "data"}
        }
    )
    assert response.status_code == 200
    assert response.json()["queue"] == "test" 