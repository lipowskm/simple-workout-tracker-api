import pytest
from async_asgi_testclient import TestClient

from app import crud
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_read_existing_user(client: TestClient, superuser_token_headers: dict):
    password = "test"
    username = "test"
    email = "test@test.com"
    user_in = UserCreate(username=username, password=password, email=email, is_superuser=True)
    user_id = await crud.user.create(obj_in=user_in)
    resp = await client.get(f'/api/users/{user_id}', headers=superuser_token_headers)
    assert resp.status_code == 200
    api_user = resp.json()
    database_user = await crud.user.get(user_id)
    assert database_user
    assert api_user['id'] == database_user.id
    assert api_user['username'] == database_user.username
