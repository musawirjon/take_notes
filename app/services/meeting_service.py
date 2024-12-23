from app.jobs.process_meeting_recording_job import ProcessMeetingRecordingJob
from app.jobs.generate_meeting_summary_job import GenerateMeetingSummaryJob
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.meeting import meeting
from app.schemas.meetings import MeetingCreate, MeetingUpdate, MeetingInDB
from app.models.user import User

class MeetingService:
    @staticmethod
    async def create_meeting(db: Session, meeting_data: MeetingCreate, current_user: User) -> MeetingInDB:
        return meeting.create(db=db, obj_in=meeting_data)

    @staticmethod
    async def get_instance_meetings(
        db: Session,
        instance_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MeetingInDB]:
        return meeting.get_by_instance(db=db, instance_id=instance_id, skip=skip, limit=limit)

    @staticmethod
    async def queue_recording_processing(db: Session, meeting_id: str):
        """Queue a job to process the meeting recording"""
        return await ProcessMeetingRecordingJob.dispatch(
            db,
            meeting_id=meeting_id
        )

    @staticmethod
    async def queue_summary_generation(db: Session, meeting_id: str):
        """Queue a job to generate meeting summary"""
        return await GenerateMeetingSummaryJob.dispatch(
            db,
            meeting_id=meeting_id
        )

    @staticmethod
    async def update_meeting_summary(
        db: Session,
        meeting_id: str,
        summary: str
    ) -> MeetingInDB:
        return meeting.update_summary(db=db, meeting_id=meeting_id, summary=summary) 