from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.notes import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.auth.security import generate_uuid
import app.crud.notes as note
from app.models.user import User

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

    @staticmethod
    async def create_note(db: Session, *, note_in: NoteCreate, current_user: User):
        # Add any preprocessing of note content here
        note_data = note_in.dict()
        note_data["user_id"] = current_user.id
        
        # You could add AI processing here
        if note_data.get("content"):
            note_data["summary"] = await process_note_content(note_data["content"])
        
        return note.create(db=db, obj_in=note_data)

    @staticmethod
    async def get_user_notes(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ):
        if search:
            return note.search_notes(db=db, user_id=user_id, search_term=search)
        return note.get_by_user(db=db, user_id=user_id, skip=skip, limit=limit)

    @staticmethod
    async def process_note_content(content: str) -> str:
        # Add AI processing logic here
        # Example: Summarization, keyword extraction, etc.
        return content 