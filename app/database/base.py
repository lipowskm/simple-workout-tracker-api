import os

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base, declared_attr

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
