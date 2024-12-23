import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.auth.jwt import create_access_token
from app.models.note import Note

@pytest.fixture
def test_note_data():
    return {
        "title": "Test Note",
        "content": "This is a test note content"
    }

@pytest.fixture
def test_note(db, test_user):
    note = Note(
        id="test-note-id",
        title="Test Note",
        content="This is a test note content",
        user_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token({"sub": test_user.id})
    return {"Authorization": f"Bearer {access_token}"}

class TestNoteEndpoints:
    def test_create_note(self, client, auth_headers, test_note_data):
        response = client.post(
            "/notes",
            headers=auth_headers,
            json=test_note_data
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_note_data["title"]
        assert data["content"] == test_note_data["content"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_notes(self, client, auth_headers, test_note):
        response = client.get("/notes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == test_note.id
        assert data[0]["title"] == test_note.title
        assert data[0]["content"] == test_note.content

    def test_get_note(self, client, auth_headers, test_note):
        response = client.get(f"/notes/{test_note.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_note.id
        assert data["title"] == test_note.title
        assert data["content"] == test_note.content

    def test_update_note(self, client, auth_headers, test_note):
        update_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = client.put(
            f"/notes/{test_note.id}",
            headers=auth_headers,
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_note.id
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]

    def test_delete_note(self, client, auth_headers, test_note):
        response = client.delete(
            f"/notes/{test_note.id}",
            headers=auth_headers
        )
        assert response.status_code == 204

        # Verify note is deleted
        response = client.get(f"/notes/{test_note.id}", headers=auth_headers)
        assert response.status_code == 404

class TestNoteAuthorization:
    def test_unauthorized_access(self, client, test_note_data):
        # Try without auth token
        endpoints = [
            ("POST", "/notes"),
            ("GET", "/notes"),
            ("GET", "/notes/test-id"),
            ("PUT", "/notes/test-id"),
            ("DELETE", "/notes/test-id"),
        ]
        
        for method, endpoint in endpoints:
            if method == "POST" or method == "PUT":
                response = client.request(method, endpoint, json=test_note_data)
            else:
                response = client.request(method, endpoint)
            assert response.status_code == 401

    def test_access_other_user_note(self, client, test_note):
        # Create another user's token
        other_user_token = create_access_token({"sub": "other-user-id"})
        headers = {"Authorization": f"Bearer {other_user_token}"}

        # Try to access note
        response = client.get(f"/notes/{test_note.id}", headers=headers)
        assert response.status_code == 404

        # Try to update note
        response = client.put(
            f"/notes/{test_note.id}",
            headers=headers,
            json={"title": "Hacked title", "content": "Hacked content"}
        )
        assert response.status_code == 404

        # Try to delete note
        response = client.delete(f"/notes/{test_note.id}", headers=headers)
        assert response.status_code == 404

class TestNoteValidation:
    def test_create_note_validation(self, client, auth_headers):
        # Test empty title
        response = client.post(
            "/notes",
            headers=auth_headers,
            json={"title": "", "content": "Content"}
        )
        assert response.status_code == 422

        # Test missing content
        response = client.post(
            "/notes",
            headers=auth_headers,
            json={"title": "Title"}
        )
        assert response.status_code == 422

    def test_update_note_validation(self, client, auth_headers, test_note):
        # Test empty title
        response = client.put(
            f"/notes/{test_note.id}",
            headers=auth_headers,
            json={"title": ""}
        )
        assert response.status_code == 422

    def test_invalid_note_id(self, client, auth_headers):
        response = client.get("/notes/invalid-id", headers=auth_headers)
        assert response.status_code == 404 

@pytest.mark.asyncio
async def test_note_processing_job(auth_client, db):
    # Create a note with processing
    response = auth_client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "This is a test note that needs processing",
            "process_content": True  # Trigger background job
        }
    )
    assert response.status_code == 200
    note_id = response.json()["id"]

    # Check if job was created
    jobs_response = auth_client.get("/api/jobs/")
    assert any(
        job["payload"].get("note_id") == note_id 
        for job in jobs_response.json()
    )