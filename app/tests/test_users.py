from typing import Dict

import pytest
from async_asgi_testclient import TestClient

from app import crud
from app.core import config
from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.tests.factories.user_factory import UserFactory, UserCreateFactory

users = UserFactory.create_batch(5)
users_create = UserCreateFactory.create_batch(5)


def verify_user_fields(api_user: dict, database_user: User):
    assert api_user['id'] == database_user.id
    assert api_user['username'] == database_user.username
    assert api_user['email'] == database_user.email
    assert api_user['first_name'] == database_user.first_name
    assert api_user['last_name'] == database_user.last_name
    assert api_user['is_active'] == database_user.is_active
    assert api_user['is_email_verified'] == database_user.is_email_verified
    assert api_user['is_superuser'] == database_user.is_superuser


def test_user_fixture(user):
    assert isinstance(user, User)


def test_user_create_fixture(user_create):
    assert isinstance(user_create, UserCreate)


@pytest.mark.asyncio
async def test_get_users_superuser_me(client: TestClient,
                                      superuser_token_headers: Dict[str, str]):
    resp = await client.get("/api/users/me", headers=superuser_token_headers)
    current_user = resp.json()
    assert current_user
    assert current_user['is_active'] is True
    assert current_user['is_superuser'] is True
    assert current_user['username'] == config.SUPERUSER


@pytest.mark.asyncio
@pytest.mark.parametrize('user', users_create)
async def test_read_existing_user(user: UserCreate,
                                  client: TestClient,
                                  superuser_token_headers: Dict[str, str]):
    user_id = await crud.user.create(obj_in=user)
    resp = await client.get(f'/api/users/{user_id}', headers=superuser_token_headers)
    assert 200 <= resp.status_code < 300
    api_user = resp.json()
    database_user = await crud.user.get(user_id)
    assert database_user
    verify_user_fields(api_user, database_user)


@pytest.mark.asyncio
@pytest.mark.parametrize('user', users_create)
async def test_verify_password_hash(user: UserCreate,
                                    client: TestClient,
                                    superuser_token_headers: Dict[str, str]):
    user_id = await crud.user.create(obj_in=user)
    database_user = await crud.user.get(user_id)
    assert database_user
    verify_password(user.password, database_user.hashed_password)
