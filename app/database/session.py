import os

import databases
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

engine = create_engine(config.DATABASE_URL, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = databases.Database(url=config.DATABASE_URL, ssl='allow')
