from typing import List, Generic, TypeVar, Type

from asyncpg import Record
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.database.base import Base
from app.database.session import database

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, id: int) -> Record:
        query = self.model.__table__.select().where(id == self.model.id)
        return await database.fetch_one(query=query)

    async def get_multi(self, skip=0, limit=100) -> List[Record]:
        query = self.model.__table__.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def create(self, obj_in: CreateSchemaType) -> int:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        query = self.model.__table__.insert().values(**db_obj)
        return await database.execute(query=query)

    async def update(self, id: int, obj_in: UpdateSchemaType) -> int:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        query = (
            self.model.__table__.update().where(id == self.model.id).values(**db_obj).returning(self.model.id)
        )
        return await database.execute(query=query)

    async def remove(self, id: int) -> None:
        query = self.model.__table__.delete().where(id == self.model.id)
        return await database.execute(query=query)
