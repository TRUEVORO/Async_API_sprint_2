import pytest
from aiohttp import ClientSession
from pydantic import AnyUrl


@pytest.fixture
def make_get_request():
    """Provides a function for making GET requests using the aiohttp session."""

    async def inner(url: AnyUrl, query_data: dict) -> tuple[any, int]:
        async with ClientSession() as session:
            async with session.get(url, params=query_data) as response:
                return await response.json(), response.status

    return inner
