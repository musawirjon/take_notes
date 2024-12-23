from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.models.meeting import Meeting
from app.schemas.meetings import MeetingCreate, MeetingUpdate

class CRUDMeeting:
    def create(self, db: Session, *, obj_in: MeetingCreate) -> Meeting:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Meeting(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_instance(
        self, db: Session, *, instance_id: str, skip: int = 0, limit: int = 100
    ) -> List[Meeting]:
        return db.query(Meeting)\
                 .filter(Meeting.instance_id == instance_id)\
                 .offset(skip)\
                 .limit(limit)\
                 .all()

    def update_summary(
        self, db: Session, *, meeting_id: str, summary: str
    ) -> Meeting:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        meeting.summary = summary
        db.commit()
        db.refresh(meeting)
        return meeting

meeting = CRUDMeeting() 