from typing import Dict
import pytest
from async_asgi_testclient import TestClient
from app.database.base import Base
from app.database.init_database import init_database
from app.database.session import engine
from app.main import app
from app.tests.factories.user_factory import UserFactory, UserCreateFactory
from app.tests.utils.user import get_superuser_token_headers
from pytest_factoryboy import register

register(UserFactory)
register(UserCreateFactory)


@pytest.fixture(scope="module")
def client() -> TestClient:
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
async def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest.fixture(scope='session', autouse=True)
async def create_test_database():
    """
    Create a clean database for test session and drop it afterwards.
    """
    Base.metadata.create_all(engine)  # Create the tables
    await init_database()  # Create superuser
    yield  # Run the tests
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function', autouse=True)
async def cleanup_database():
    """
    Cleanup database after each test case
    """
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    await init_database()
