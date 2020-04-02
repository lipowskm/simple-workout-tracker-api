from typing import Optional

from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    default_reps: Optional[int] = 8


class ExerciseBaseInDB(ExerciseBase):
    id: int = None


class ExerciseCreate(ExerciseBase):
    name: str


class ExerciseUpdate(ExerciseBase):
    pass


class Exercise(ExerciseBaseInDB):
    pass
