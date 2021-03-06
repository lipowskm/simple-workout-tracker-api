from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, index=True)
    is_active = Column(Boolean(), default=True)
    is_email_verified = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
