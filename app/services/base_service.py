from typing import Generic, TypeVar, Type, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.base import CRUDBase
from app.models.base import Base
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud_class: Type[CRUDBase]):
        self.crud = crud_class

    async def get(self, db: Session, id: str) -> ModelType:
        obj = self.crud.get(db=db, id=id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.crud.model.__name__} not found")
        return obj

    async def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.crud.get_multi(db=db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        return self.crud.create(db=db, obj_in=obj_in)

    async def update(self, db: Session, *, id: str, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = await self.get(db=db, id=id)
        return self.crud.update(db=db, db_obj=db_obj, obj_in=obj_in)

    async def delete(self, db: Session, *, id: str) -> ModelType:
        return self.crud.remove(db=db, id=id) 