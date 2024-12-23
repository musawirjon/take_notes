from sqlalchemy.orm import Session
from app.models.notes import Note
from app.schemas.note import NoteCreate, NoteUpdate
from datetime import datetime

def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()

def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: NoteCreate, user_id: int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db_note.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False 