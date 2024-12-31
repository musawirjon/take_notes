from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.instance import InstanceCreate, InstanceUpdate, InstanceOut
from app.services.instance_service import InstanceService
from app.database import get_db
import uuid

router = APIRouter()

@router.post("/", response_model=InstanceOut, status_code=status.HTTP_201_CREATED)
def create_instance(
    account_id: uuid.UUID, 
    instance_data: InstanceCreate, 
    db: Session = Depends(get_db)
):
    instance_service = InstanceService(db)
    instance = instance_service.create_instance(account_id, instance_data)
    return instance

@router.get("/{instance_id}", response_model=InstanceOut)
def get_instance(instance_id: uuid.UUID, db: Session = Depends(get_db)):
    instance_service = InstanceService(db)
    instance = instance_service.get_instance_by_id(instance_id)
    return instance

@router.put("/{instance_id}", response_model=InstanceOut)
def update_instance(
    instance_id: uuid.UUID,
    instance_data: InstanceUpdate,
    db: Session = Depends(get_db)
):
    instance_service = InstanceService(db)
    instance = instance_service.update_instance(instance_id, instance_data)
    return instance

@router.delete("/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instance(instance_id: uuid.UUID, db: Session = Depends(get_db)):
    instance_service = InstanceService(db)
    instance_service.delete_instance(instance_id)
    return {"detail": "Instance deleted"}
