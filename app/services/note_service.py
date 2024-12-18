from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.auth.security import generate_uuid

class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, note_id: str) -> Optional[Note]:
        return self.db.query(Note).filter(Note.id == note_id).first()

    def get_user_notes(self, user_id: str) -> List[Note]:
        return self.db.query(Note).filter(Note.user_id == user_id).all()

    def create(self, user_id: str, note_data: NoteCreate) -> Note:
        note = Note(
            id=generate_uuid(),
            user_id=user_id,
            **note_data.dict()
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: Note, note_data: NoteUpdate) -> Note:
        for key, value in note_data.dict(exclude_unset=True).items():
            setattr(note, key, value)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit() 