from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import schemas
from ..crud import notes

router = APIRouter()

@router.get("/notes/", response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Get user_id from JWT token
    user_id = 1  # Placeholder
    return notes.get_notes(db, user_id=user_id, skip=skip, limit=limit)

@router.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    # TODO: Get user_id from JWT token
    user_id = 1  # Placeholder
    return notes.create_note(db=db, note=note, user_id=user_id)

@router.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    # TODO: Get user_id from JWT token
    user_id = 1  # Placeholder
    db_note = notes.update_note(db=db, note_id=note_id, note=note, user_id=user_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    # TODO: Get user_id from JWT token
    user_id = 1  # Placeholder
    success = notes.delete_note(db=db, note_id=note_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"} 