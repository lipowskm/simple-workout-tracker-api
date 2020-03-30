from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app import crud
from app.api.utils.security import get_current_active_user, get_current_active_superuser
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        current_user: DBUser = Depends(get_current_active_superuser),
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve users.
    """
    return await crud.user.get_multi(skip, limit)


@router.post("/", response_model=User)
async def create_user(
        user_in: UserCreate,
        current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Create new user.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Username already taken.",
        )
    user_id = await crud.user.create(obj_in=user_in)
    return await crud.user.get(user_id)


@router.get("/me", response_model=User)
async def read_user_me(current_user: DBUser = Depends(get_current_active_user)):
    """
    Get current user
    """
    return current_user


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
        user_id: int,
        current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Get a specific user by id.
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
        user_id: int,
        user_in: UserUpdate,
        current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Update a user.
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    other_user = await crud.user.get_by_email(email=user_in.email)
    if other_user and (user != other_user):
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )
    other_user = await crud.user.get_by_username(username=user_in.username)
    if other_user and (user != other_user):
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Username already taken.",
        )
    user_id = await crud.user.update(id=user_id, obj_in=user_in)
    return await crud.user.get(id=user_id)


@router.delete("/{user_id}", response_model=User)
async def remove_user_by_id(
        user_id: int,
        current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Remove a specific user by id
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    await crud.user.remove(id=user_id)
    return user
