import pytest
from uuid import uuid4
from datetime import datetime

@pytest.mark.asyncio
async def test_create_meeting(auth_client, db):
    response = auth_client.post(
        "/api/meetings/",
        json={
            "title": "Test Meeting",
            "scheduled_at": datetime.utcnow().isoformat(),
            "duration_minutes": 60,
            "instance_id": str(uuid4())
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meeting"

@pytest.mark.asyncio
async def test_meeting_recording_processing(auth_client, db):
    # Create meeting
    meeting_response = auth_client.post(
        "/api/meetings/",
        json={
            "title": "Test Meeting",
            "scheduled_at": datetime.utcnow().isoformat(),
            "duration_minutes": 60,
            "instance_id": str(uuid4())
        }
    )
    meeting_id = meeting_response.json()["id"]

    # Test recording upload and processing
    response = auth_client.post(
        f"/api/meetings/{meeting_id}/recording",
        files={
            "file": ("recording.mp4", b"test content", "video/mp4")
        }
    )
    assert response.status_code == 200
    
    # Check if processing job was created
    jobs_response = auth_client.get("/api/jobs/")
    assert any(
        job["payload"].get("meeting_id") == meeting_id 
        for job in jobs_response.json()
    )

@pytest.mark.asyncio
async def test_meeting_transcription(auth_client, db):
    # Create meeting
    meeting_response = auth_client.post(
        "/api/meetings/",
        json={
            "title": "Test Meeting",
            "scheduled_at": datetime.utcnow().isoformat(),
            "duration_minutes": 60,
            "instance_id": str(uuid4())
        }
    )
    meeting_id = meeting_response.json()["id"]

    # Test real-time transcription
    response = auth_client.post(
        f"/api/meetings/{meeting_id}/transcribe",
        json={
            "speaker": "Test User",
            "content": "This is a test transcription"
        }
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_meeting_summary(auth_client, db):
    # Create meeting with transcriptions
    meeting_id = str(uuid4())
    
    # Request summary generation
    response = auth_client.post(
        f"/api/meetings/{meeting_id}/summary"
    )
    assert response.status_code == 200
    
    # Verify summary job creation
    jobs_response = auth_client.get("/api/jobs/")
    assert any(
        job["queue"] == "summaries" and 
        job["payload"].get("meeting_id") == meeting_id 
        for job in jobs_response.json()
    ) 

# Make sure all controllers are using services properly
class MeetingController:
    def __init__(self):
        self.meeting_service = MeetingService()
        self.realtime_service = RealtimeService()
        self.job_service = JobDispatcher()  # Add if missing

    async def create_meeting(self, db: Session, meeting_data: MeetingCreate):
        return await self.meeting_service.create_meeting(db, meeting_data)