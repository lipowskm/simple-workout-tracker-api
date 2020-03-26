from typing import List

from fastapi import APIRouter
from fastapi_sqlalchemy import db

from app.models.user import User
from app.schemas.user import UserBase

router = APIRouter()


@router.post("/", response_model=UserBase)
async def create_user(user: UserBase):
    """
    Create new user.
    """
    db_user = User(
        first_name=user.first_name, last_name=user.last_name, email=user.email,
        is_active=user.is_active, is_superuser=user.is_superuser
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserBase])
async def read_users():
    """
    Retrieve users.
    """
    return db.session.query(User).all()


@router.get("/{user_id}", response_model=UserBase)
def read_user_by_id(user_id: int):
    """
    Get a specific user by id.
    """
    return db.session.query(User).filter(user_id == User.id).first()
