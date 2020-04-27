from async_asgi_testclient import TestClient

from app.core import config


async def get_superuser_token_headers(client: TestClient):
    login_data = {
        "username": config.SUPERUSER,
        "password": config.SUPERUSER_PASSWORD
    }
    r = await client.post("/api/login/access-token", form=login_data)
    tokens = r.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers

