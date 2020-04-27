from typing import Dict

import pytest
from async_asgi_testclient import TestClient

from app.database.base import Base
from app.database.init_database import init_database
from app.database.session import engine
from app.main import app
from app.tests.utils.user import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
async def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """
  Create a clean database on every test case.
  """
    Base.metadata.drop_all(engine)  # Delete all data from database
    Base.metadata.create_all(engine)  # Create the tables
    await init_database()  # Create superuser
    yield  # Run the tests
