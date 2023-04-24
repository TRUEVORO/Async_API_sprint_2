from abc import ABC, abstractmethod
from uuid import UUID


class AsyncBaseStorage(ABC):
    """An abstract async storage."""

    @abstractmethod
    async def save_data(self, key: str | UUID, value: any, cache_lifetime: int) -> None:
        """Save data in storage."""

        raise NotImplementedError

    @abstractmethod
    async def retrieve_data(self, key: str | UUID) -> any:
        """Retrieve data from storage."""

        raise NotImplementedError
