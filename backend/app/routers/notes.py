from fastapi import APIRouter, Depends, status
from typing import List
from backend.app.controllers.note_controller import NoteController
from backend.app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    controller: NoteController = Depends()
):
    return await controller.create_note(note_data)

@router.get("", response_model=List[NoteResponse])
async def get_notes(
    controller: NoteController = Depends()
):
    return await controller.get_notes()

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    controller: NoteController = Depends()
):
    return await controller.get_note(note_id)

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    controller: NoteController = Depends()
):
    return await controller.update_note(note_id, note_data)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    controller: NoteController = Depends()
):
    return await controller.delete_note(note_id) 