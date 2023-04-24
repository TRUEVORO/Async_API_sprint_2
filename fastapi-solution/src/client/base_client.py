from abc import ABC


class AsyncBaseClient(ABC):
    """An async abstract client."""

    def __init__(self, connection: any = None):
        """Initialization of async base client."""

        self.connection = connection

    async def close(self) -> None:
        """Close async client connection."""

        if self.connection:
            await self.connection.close()
