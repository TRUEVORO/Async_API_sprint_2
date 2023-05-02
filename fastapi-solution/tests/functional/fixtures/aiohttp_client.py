from typing import AsyncGenerator

import pytest
from aiohttp import ClientSession
from pydantic import AnyUrl


@pytest.fixture(scope='session')
async def aiohttp_session(loop) -> AsyncGenerator[ClientSession, None]:
    """Provides an instance of the aiohttp ClientSession for the test session."""

    async with ClientSession() as session:
        yield session


@pytest.fixture
def make_get_request():
    """Provides a function for making GET requests using the aiohttp session."""

    async def inner(url: AnyUrl, query_data: dict) -> tuple[any, int]:
        async with ClientSession() as session:  # HELP: Пытался использовать фикстуру aiohttp_session,
            #  чтобы не плодить сессии, но постоянно падала ошибка
            #  AttributeError: 'async_generator' object has no attribute 'get',
            #  буду очень благодарен, если получится помочь
            async with session.get(url, params=query_data) as response:
                return await response.json(), response.status

    return inner
