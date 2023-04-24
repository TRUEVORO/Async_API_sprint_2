from client import AsyncRedisClient

from .base_storage import AsyncBaseStorage


class AsyncRedisStorage(AsyncBaseStorage):
    """An async Redis storage."""

    def __init__(self, redis_client: AsyncRedisClient) -> None:
        """Initialize async Redis storage."""

        self.redis = redis_client

    async def save_data(self, key: str, value: str, cache_lifetime: int) -> None:
        """Save data in Redis."""

        await self.redis.set(name=key, value=value, ex=cache_lifetime)

    async def retrieve_data(self, key: str) -> str | bytes | None:
        """Retrieve data from Redis."""

        return await self.redis.get(key)
