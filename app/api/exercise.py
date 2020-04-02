from typing import List

from starlette.status import HTTP_409_CONFLICT

from app import crud
from fastapi import APIRouter, HTTPException

from app.schemas.exercise import Exercise, ExerciseCreate

router = APIRouter()


@router.get("", response_model=List[Exercise])
async def read_exercises(
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve exercises.
    """
    return await crud.exercise.get_multi(skip, limit)


@router.post("", response_model=Exercise)
async def create_exercise(
        exercise_in: ExerciseCreate
):
    """
    Create new exercise.
    """
    exercise = await crud.exercise.get_by_name(name=exercise_in.name)
    if exercise:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The exercise with this name already exists in the system.",
        )
    exercise_id = await crud.exercise.create(obj_in=exercise_in)
    return await crud.exercise.get(exercise_id)
