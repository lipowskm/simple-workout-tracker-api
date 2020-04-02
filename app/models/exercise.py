from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Exercise(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    default_reps = Column(Integer, default=8)
