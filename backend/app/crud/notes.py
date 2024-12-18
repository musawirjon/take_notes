from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas
from datetime import datetime

def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(models.Note.user_id == user_id).offset(skip).limit(limit).all()

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: schemas.NoteCreate, user_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db_note.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False 