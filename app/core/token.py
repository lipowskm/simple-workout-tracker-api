from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi.encoders import jsonable_encoder
from jwt import InvalidTokenError

from app import crud
from app.core import config
from app.schemas.user import User, UserCreate, UserUpdate

ALGORITHM = "HS256"
access_token_jwt_subject = "access"
register_token_jwt_subject = "register"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_register_token(*, user: UserCreate, expires_delta: timedelta = None):
    to_encode = jsonable_encoder(user)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire, "sub": register_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_register_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == register_token_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None
    except AssertionError:
        return None


def generate_password_reset_token(email, subject):
    delta = timedelta(hours=config.EMAIL_RESET_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": subject, "email": email},
        config.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


async def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        record = await crud.user.get_by_email(email=decoded_token["email"])
        subject = User(**record).id
        assert decoded_token["sub"] == subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None
    except AssertionError:
        return None
