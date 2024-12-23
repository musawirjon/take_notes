import pytest
from fastapi.testclient import TestClient
from app.auth.jwt import create_access_token

def test_get_current_user(client, test_user, test_user_data):
    access_token = create_access_token({"sub": test_user.id})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]

def test_update_user(client, test_user, test_user_data):
    access_token = create_access_token({"sub": test_user.id})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    update_data = {
        "full_name": "Updated Name",
        "email": "updated@example.com"
    }
    
    response = client.put("/users/me", headers=headers, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == update_data["email"]

def test_delete_user(client, test_user):
    access_token = create_access_token({"sub": test_user.id})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 204

def test_unauthorized_access(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    
    response = client.put("/users/me", json={"full_name": "Test"})
    assert response.status_code == 401
    
    response = client.delete("/users/me")
    assert response.status_code == 401 

@pytest.mark.asyncio
async def test_user_notification_job(auth_client, db):
    # Test user notification job creation
    response = auth_client.post(
        "/api/users/notify",
        json={
            "user_id": str(test_user.id),
            "message": "Test notification"
        }
    )
    assert response.status_code == 200

    # Verify job creation
    jobs_response = auth_client.get("/api/jobs/")
    jobs = jobs_response.json()
    assert any(
        job["queue"] == "notifications" 
        for job in jobs
    )

@pytest.mark.asyncio
async def test_user_background_tasks(auth_client, db):
    # Test background task for user data processing
    response = auth_client.post(
        f"/api/users/{test_user.id}/process",
        json={
            "task_type": "data_analysis"
        }
    )
    assert response.status_code == 200

    # Check job status
    job_id = response.json()["job_id"]
    job_status = auth_client.get(f"/api/jobs/{job_id}")
    assert job_status.json()["status"] in ["pending", "processing"]