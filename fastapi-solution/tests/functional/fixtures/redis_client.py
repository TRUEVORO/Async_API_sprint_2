import pytest
from redis.asyncio import Redis
from tests.functional.settings import test_settings


@pytest.fixture(scope='session')
async def redis_client():
    client = Redis(
        host=test_settings.redis_dsn.host, port=int(test_settings.redis_dsn.port), db=test_settings.redis_dsn.path[1:]
    )
    yield client
    await client.close()


@pytest.fixture
async def redis_clean_data(redis_client):
    await redis_client.flushdb()
    yield
    await redis_client.flushdb()
