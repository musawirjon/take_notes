from sqlalchemy.orm import Session
from app.models.instance import Instance
from app.schemas.instance import InstanceCreate, InstanceUpdate
from fastapi import HTTPException, status
import uuid

class InstanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_instance_by_id(self, instance_id: uuid.UUID) -> Instance:
        instance = self.db.query(Instance).filter(Instance.id == instance_id).first()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Instance not found"
            )
        return instance

    def create_instance(self, account_id: uuid.UUID, instance_data: InstanceCreate) -> Instance:
        # Ensure the Account exists (you may want to add validation logic here)
        instance = Instance(
            name=instance_data.name,
            description=instance_data.description,
            is_active=instance_data.is_active,
            ai_settings=instance_data.ai_settings,
            account_id=account_id
        )
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update_instance(self, instance_id: uuid.UUID, instance_data: InstanceUpdate) -> Instance:
        instance = self.get_instance_by_id(instance_id)
        for key, value in instance_data.dict(exclude_unset=True).items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete_instance(self, instance_id: uuid.UUID) -> None:
        instance = self.get_instance_by_id(instance_id)
        self.db.delete(instance)
        self.db.commit()
