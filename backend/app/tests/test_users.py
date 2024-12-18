import pytest
from fastapi.testclient import TestClient
from backend.app.auth.jwt import create_access_token

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