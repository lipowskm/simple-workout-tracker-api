from app import crud
from app.core import config
from app.schemas.user import SuperUserCreate

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
from app.database import base


async def init_database():
    user = await crud.user.get_by_username(username=config.SUPERUSER)
    if not user:
        user_in = SuperUserCreate(
            username=config.SUPERUSER,
            password=config.SUPERUSER_PASSWORD,
            email='admin@admin.com',
            is_superuser=True
        )
        await crud.user.create(obj_in=user_in)
