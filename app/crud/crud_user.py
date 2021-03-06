from datetime import datetime

from asyncpg import Record
from fastapi.encoders import jsonable_encoder

from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.database.session import database
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, email: str) -> Record:
        query = self.model.__table__.select().where(email.lower() == self.model.email)
        return await database.fetch_one(query=query)

    async def get_by_username(self, username: str) -> Record:
        query = self.model.__table__.select().where(username == self.model.username)
        return await database.fetch_one(query=query)

    async def create(self, obj_in: UserCreate) -> int:
        query = self.model.__table__.insert().values(email=obj_in.email.lower(),
                                                     username=obj_in.username,
                                                     hashed_password=get_password_hash(obj_in.password),
                                                     first_name=obj_in.first_name,
                                                     last_name=obj_in.last_name,
                                                     date_created=datetime.utcnow(),
                                                     is_email_verified=obj_in.is_email_verified,
                                                     is_superuser=obj_in.is_superuser,
                                                     is_active=obj_in.is_active).returning(self.model.id)
        return await database.execute(query=query)

    async def update(self, id: int, obj_in: UserUpdate) -> int:
        obj_in_data = jsonable_encoder(obj_in)
        if 'password' in obj_in_data.keys() and obj_in_data['password']:
            obj_in_data['hashed_password'] = get_password_hash(obj_in_data.pop('password'))
        elif 'hashed_password' in obj_in_data:
            obj_in_data['hashed_password'] = None
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
