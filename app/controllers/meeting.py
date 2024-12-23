from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.meeting_service import MeetingService
from app.services.realtime_service import RealtimeService
from app.services.job_dispatcher import JobDispatcher
from app.schemas.meetings import MeetingCreate, MeetingUpdate, MeetingInDB
from app.models.user import User
from typing import List

class MeetingController:
    def __init__(self):
        self.meeting_service = MeetingService()
        self.realtime_service = RealtimeService()
        self.job_service = JobDispatcher()

    async def create_meeting(
        self,
        db: Session,
        meeting_data: MeetingCreate,
        current_user: User
    ) -> MeetingInDB:
        return await self.meeting_service.create_meeting(
            db=db,
            meeting_data=meeting_data,
            current_user=current_user
        )

    async def get_instance_meetings(
        self,
        db: Session,
        instance_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[MeetingInDB]:
        return await self.meeting_service.get_instance_meetings(
            db=db,
            instance_id=instance_id,
            current_user=current_user,
            skip=skip,
            limit=limit
        )

    async def end_meeting(self, db: Session, meeting_id: str):
        return await self.meeting_service.end_meeting(db, meeting_id)

    async def process_transcription(self, meeting_id: str, speaker: str, content: str):
        return await self.meeting_service.process_transcription(meeting_id, speaker, content)

    async def update_meeting_notes(self, meeting_id: str, note_data: dict):
        return await self.meeting_service.update_meeting_notes(meeting_id, note_data)

    async def handle_websocket(self, websocket):
        await self.realtime_service.handle_websocket(websocket)

    async def process_meeting_recording(
        self,
        db: Session,
        meeting_id: str,
        current_user: User
    ):
        # Verify meeting access here
        job = await self.meeting_service.queue_recording_processing(db, meeting_id)
        return {"job_id": str(job.id), "status": "processing"}

    async def generate_meeting_summary(
        self,
        db: Session,
        meeting_id: str,
        current_user: User
    ):
        # Verify meeting access here
        job = await self.meeting_service.queue_summary_generation(db, meeting_id)
        return {"job_id": str(job.id), "status": "processing"}