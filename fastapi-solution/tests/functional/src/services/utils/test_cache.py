from unittest.mock import AsyncMock

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from src.services.utils import cache
from src.storage import AsyncBaseStorage

pytestmark = pytest.mark.asyncio


async def sample_async_function(*args, **kwargs):
    return f"Result: {args}, {kwargs}"


async def test_cache_hit():
    storage = AsyncMock(spec=AsyncBaseStorage)
    storage.retrieve_data = AsyncMock(return_value=None)
    storage.save_data = AsyncMock()

    cached_function = cache(storage, RedisConnectionError)(sample_async_function)

    result = await cached_function(1, 2, kwarg='test')

    assert result == 'Result: {}, {}'.format((1, 2), {'kwarg': 'test'})
    storage.retrieve_data.assert_called_once()
    storage.save_data.assert_called_once()
