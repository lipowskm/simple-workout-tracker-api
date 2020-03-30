from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app import crud
from app.api.utils.security import get_current_user
from app.core import config
from app.core.token import create_access_token
from app.models.user import User as DBUser
from app.schemas.token import Token
from app.schemas.user import User

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


@router.post("/login/test-token", tags=["login"], response_model=User)
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
