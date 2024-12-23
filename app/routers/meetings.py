from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.dependencies import get_current_user
from app.controllers.meeting import MeetingController
from app.schemas.meetings import MeetingCreate, MeetingUpdate, MeetingInDB
from app.models.user import User
from app.database import get_db

router = APIRouter(
    prefix="/meetings",
    tags=["meetings"]
)

meeting_controller = MeetingController()

@router.post("/", response_model=MeetingInDB)
async def create_meeting(
    *,
    db: Session = Depends(get_db),
    meeting_in: MeetingCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create new meeting.
    """
    return await meeting_controller.create_meeting(
        db=db,
        meeting_data=meeting_in,
        current_user=current_user
    )

@router.get("/instance/{instance_id}", response_model=List[MeetingInDB])
async def get_instance_meetings(
    instance_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve meetings for an instance.
    """
    return await meeting_controller.get_instance_meetings(
        db=db,
        instance_id=instance_id,
        current_user=current_user,
        skip=skip,
        limit=limit
    )

@router.get("/{meeting_id}", response_model=MeetingInDB)
def get_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get meeting by ID.
    """
    meeting_obj = meeting.get(db=db, id=meeting_id)
    if not meeting_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    if meeting_obj.instance_id != current_user.instance_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't have permission for this meeting"
        )
    return meeting_obj

@router.put("/{meeting_id}", response_model=MeetingInDB)
def update_meeting(
    *,
    db: Session = Depends(get_db),
    meeting_id: str,
    meeting_in: MeetingUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update meeting.
    """
    meeting_obj = meeting.get(db=db, id=meeting_id)
    if not meeting_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    if meeting_obj.instance_id != current_user.instance_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't have permission for this meeting"
        )
    return meeting.update(db=db, db_obj=meeting_obj, obj_in=meeting_in)

@router.delete("/{meeting_id}", response_model=MeetingInDB)
def delete_meeting(
    *,
    db: Session = Depends(get_db),
    meeting_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete meeting.
    """
    meeting_obj = meeting.get(db=db, id=meeting_id)
    if not meeting_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    if meeting_obj.instance_id != current_user.instance_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't have permission for this meeting"
        )
    return meeting.remove(db=db, id=meeting_id)

@router.post("/{meeting_id}/process-recording")
async def process_meeting_recording(
    meeting_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await meeting_controller.process_meeting_recording(
        db=db,
        meeting_id=meeting_id,
        current_user=current_user
    )

@router.post("/{meeting_id}/generate-summary")
async def generate_meeting_summary(
    meeting_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await meeting_controller.generate_meeting_summary(
        db=db,
        meeting_id=meeting_id,
        current_user=current_user
    ) 