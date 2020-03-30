from asyncpg import Record
from fastapi.encoders import jsonable_encoder

from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.database.session import database
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, email: str) -> Record:
        query = self.model.__table__.select().where(email == self.model.email)
        return await database.fetch_one(query=query)

    async def get_by_username(self, username: str) -> Record:
        query = self.model.__table__.select().where(username == self.model.username)
        return await database.fetch_one(query=query)

    async def create(self, obj_in: UserCreate) -> int:
        """
        Returns user id for some reason
        :param obj_in:
        :return: user id
        """
        query = self.model.__table__.insert().values(email=obj_in.email,
                                                     username=obj_in.username,
                                                     hashed_password=get_password_hash(obj_in.password),
                                                     first_name=obj_in.first_name,
                                                     last_name=obj_in.last_name,
                                                     is_superuser=obj_in.is_superuser,
                                                     is_active=obj_in.is_active).returning(self.model.id)
        return await database.execute(query=query)

    async def update(self, id: int, obj_in: UserUpdate) -> Record:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data['password']:
            obj_in_data['hashed_password'] = get_password_hash(obj_in_data.pop('password'))
        else:
            obj_in_data['hashed_password'] = obj_in_data.pop('password')
        query = (self.model.__table__.update().where(id == self.model.id).values(
            {k: v for k, v in obj_in_data.items() if v})).returning(
            self.model.id)
        return await database.execute(query=query)

    async def authenticate(
            self, username: str, password: str
    ):
        record = await self.get_by_username(username=username)
        if not record:
            record = await self.get_by_email(email=username)
            if not record:
                return None
        user = User(**record)
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
