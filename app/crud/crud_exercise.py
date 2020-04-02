from asyncpg import Record

from app.crud.base import CRUDBase
from app.database.session import database
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    async def get_by_name(self, name: str) -> Record:
        query = self.model.__table__.select().where(name == self.model.name)
        return await database.fetch_one(query=query)


exercise = CRUDExercise(Exercise)
