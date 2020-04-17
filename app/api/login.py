from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from app import crud
from app.core import config
from app.core.token import create_access_token, generate_password_reset_token, verify_password_reset_token, \
    create_register_token, verify_register_token
from app.models.user import User as DBUser
from app.schemas.msg import Msg
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.utils.email import send_reset_password_email, send_verify_account_email, send_new_account_email

router = APIRouter()


@router.post("/login/access-token",
             tags=["login"],
             response_model=Token)
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
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Incorrect credentials")
    elif not user.is_active:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Inactive user")
    elif not user.is_email_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Please verify your account via email")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register",
             tags=["login"],
             response_model=Msg)
async def register(
        username: str = Form(...),
        password: str = Form(...),
        email: EmailStr = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(None)
):
    """
    Create new account and send verification email with token to user.
    """
    user = await crud.user.get_by_email(email=email)
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )
    user = await crud.user.get_by_username(username=username)
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Username already taken",
        )
    user = UserCreate(username=username,
                      password=password,
                      email=email,
                      first_name=first_name,
                      last_name=last_name,
                      is_email_verified=False
                      )
    user_id = await crud.user.create(user)
    register_token = create_register_token(data={"email": user.email})
    if send_verify_account_email(
            email=user.email, username=user.username, first_name=user.first_name, token=register_token
    ):
        return {"msg": "New account email sent, check your inbox to verify your account"}
    else:
        await crud.user.remove(user_id)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while trying to send email, please try again",
        )


@router.post("/verify-account",
             tags=["login"],
             response_model=Msg)
async def verify_account(
        token: str = Form(...)
):
    """
    Verify account using token.
    """
    email = await verify_register_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid email verify token")
    record = await crud.user.get_by_email(email)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system."
        )
    user = DBUser(**record)
    if user.is_email_verified:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User already verified",
        )
    await crud.user.update(user.id, {'is_email_verified': True})
    send_new_account_email(email=user.email, username=user.username, first_name=user.first_name)
    return {"msg": "Account verified"}


@router.post("/recover-password/{email}",
             tags=["login"],
             response_model=Msg,
             status_code=201)
async def recover_password(
        email: str
):
    """
    Recover password
    """
    record = await crud.user.get_by_email(email=email)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system"
        )
    user = DBUser(**record)
    password_reset_token = generate_password_reset_token(email=email, subject=user.id)
    send_reset_password_email(
        email=user.email, username=user.username, first_name=user.first_name, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/",
             tags=["login"],
             response_model=Msg)
async def reset_password(
        token: str = Body(...),
        new_password: str = Body(...)
):
    """
    Reset password
    """
    email = await verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid password reset token")
    record = await crud.user.get_by_email(email=email)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system",
        )
    user = DBUser(**record)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user.password = new_password
    await crud.user.update(user.id, user)
    return {"msg": "Password updated successfully"}
