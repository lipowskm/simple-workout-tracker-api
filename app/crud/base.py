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
        """
        Return single record from given object ID.
        :param id: Database object id.
        :return: asyncpg Record object containing data.
        """
        query = self.model.__table__.select().where(id == self.model.id)
        return await database.fetch_one(query=query)

    async def get_multi(self, skip=0, limit=100) -> List[Record]:
        """
        Return list of desired objects.
        :param skip: How many of first objects to skip in the result.
        :param limit: Max number of objects to get from query.
        :return: List of asyncpg Record objects containing data.
        """
        query = self.model.__table__.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def create(self, obj_in: CreateSchemaType) -> int:
        """
        Create object in database.
        :param obj_in: Class inheriting from pydantic BaseModel with attributes needed for object creation.
        :return: id of created object.
        """
        obj_in_data = jsonable_encoder(obj_in)
        query = self.model.__table__.insert().values(**obj_in_data)
        return await database.execute(query=query)

    async def update(self, id: int, obj_in: UpdateSchemaType) -> int:
        """
        Update object with given id.
        :param id: id of updated object in database.
        :param obj_in: Class inheriting from pydantic BaseModel with attributes needed for object update.
        :return: id of updated object in database.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        query = (
            self.model.__table__.update().where(id == self.model.id).values(**db_obj)
        )
        return await database.execute(query=query)

    async def remove(self, id: int) -> int:
        """
        Remove object with given id.
        :param id: id of object in database.
        :return: id of object in database.
        """
        query = self.model.__table__.delete().where(id == self.model.id)
        return await database.execute(query=query)

    async def remove_all(self) -> int:
        """
        Remove all rows from table.
        :param id: id of object in database.
        :return: id of object in database.
        """
        query = self.model.__table__.delete()
        return await database.execute(query=query)
