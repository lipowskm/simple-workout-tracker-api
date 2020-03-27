from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate
):
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
def read_user_me(current_user: DBUser = Depends(get_current_active_user)):
    """
    Get current user
    """
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
        user_id: int,
        db: Session = Depends(get_db)
):
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
        *,
        db: Session = Depends(get_db),
        user_id: int,
        user_in: UserUpdate
):
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=User)
def remove_user_by_id(
        user_id: int,
        db: Session = Depends(get_db)
):
    """
    Remove a specific user by id
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    user = crud.user.remove(db, id=user_id)
    return user
