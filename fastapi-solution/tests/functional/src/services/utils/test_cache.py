from unittest.mock import AsyncMock

import pytest

from src.services.utils import cache
from src.storage import AsyncBaseStorage, StorageConnectionError


async def sample_async_function(*args, **kwargs):
    return f"Result: {args}, {kwargs}"


@pytest.mark.asyncio
async def test_cache_hit():
    storage = AsyncMock(spec=AsyncBaseStorage)
    storage.retrieve_data = AsyncMock(return_value=None)
    storage.save_data = AsyncMock()

    cached_function = cache(storage)(sample_async_function)

    result = await cached_function(1, 2, kwarg='test')

    assert result == 'Result: {}, {}'.format((1, 2), {'kwarg': 'test'})
    storage.retrieve_data.assert_called_once()
    storage.save_data.assert_called_once()


@pytest.mark.asyncio
async def test_storage_connection_error():
    storage = AsyncMock(spec=AsyncBaseStorage)
    storage.retrieve_data = AsyncMock(side_effect=StorageConnectionError)
    storage.save_data = AsyncMock(side_effect=StorageConnectionError)

    cached_function = cache(storage)(sample_async_function)

    with pytest.raises(StorageConnectionError):
        await cached_function(1, 2, kwarg='test')
