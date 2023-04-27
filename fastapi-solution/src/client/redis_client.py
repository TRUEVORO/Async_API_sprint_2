from redis.typing import EncodableT, KeyT

from .base_client import AsyncBaseClient


class AsyncRedisClient(AsyncBaseClient):
    """Redis client."""

    async def set(self, name: KeyT, value: EncodableT, *args, **kwargs) -> None:
        """Redis client execute set."""

        await self.connection.set(name, value, *args, **kwargs)

    async def get(self, name: KeyT) -> bytes | None:
        """Redis client execute get."""

        return await self.connection.get(name)
