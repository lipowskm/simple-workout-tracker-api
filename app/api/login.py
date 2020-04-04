from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app import crud
from app.core import config
from app.core.security import get_password_hash
from app.core.token import create_access_token
from app.models.user import User
from app.schemas.msg import Msg
from app.schemas.token import Token
from app.utils.email import generate_password_reset_token, send_reset_password_email, verify_password_reset_token

router = APIRouter()


@router.post("/login/access-token", tags=["login"], response_model=Token)
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Incorrect login or password")
    elif not user.is_active:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}", tags=["login"], response_model=Msg)
async def recover_password(email: str):
    """
    Password Recovery
    """
    record = await crud.user.get_by_email(email=email)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system."
        )
    user = User(**record)
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email=user.email, username=user.username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", tags=["login"], response_model=Msg)
async def reset_password(token: str = Body(...), new_password: str = Body(...)):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    record = await crud.user.get_by_email(email=email)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    user = User(**record)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user.password = new_password
    await crud.user.update(user.id, user)
    return {"msg": "Password updated successfully"}


