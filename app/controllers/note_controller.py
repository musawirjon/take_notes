from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService
from app.auth.dependencies import get_current_user

class NoteController:
    def __init__(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user
        self.note_service = NoteService(db)

    async def create_note(self, note_data: NoteCreate):
        return self.note_service.create(self.current_user.id, note_data)

    async def get_notes(self):
        return self.note_service.get_user_notes(self.current_user.id)

    async def get_note(self, note_id: str):
        note = self.note_service.get_by_id(note_id)
        if not note or note.user_id != self.current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note

    async def update_note(self, note_id: str, note_data: NoteUpdate):
        note = await self.get_note(note_id)
        return self.note_service.update(note, note_data)

    async def delete_note(self, note_id: str):
        note = await self.get_note(note_id)
        self.note_service.delete(note) 