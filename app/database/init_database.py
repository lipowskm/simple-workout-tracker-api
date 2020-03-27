from app import crud
from app.core import config
from app.schemas.user import SuperUserCreate

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.database import base


def init_database(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_username(db_session, username=config.SUPERUSER)
    if not user:
        user_in = SuperUserCreate(
            username=config.SUPERUSER,
            password=config.SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db_session, obj_in=user_in)
