from gino.ext.starlette import Gino
from sqlalchemy import MetaData

from app.core import config
from app.main import app

database: MetaData = Gino(app, dsn=config.DATABASE_URL)
