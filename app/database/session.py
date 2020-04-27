import databases
from sqlalchemy import create_engine

from app.core import config

if config.TESTING:
    engine = create_engine(config.TEST_DATABASE_URL)
    database = databases.Database(url=config.TEST_DATABASE_URL, force_rollback=True)
else:
    engine = create_engine(config.DATABASE_URL)
    database = databases.Database(url=config.DATABASE_URL, ssl='allow')
