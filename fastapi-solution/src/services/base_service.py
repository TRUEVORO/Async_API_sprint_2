from abc import ABC
from uuid import UUID

from elasticsearch.exceptions import ConnectionError as ElasticsearchConnectionError
from redis.exceptions import ConnectionError as RedisConnectionError

from client import AsyncElasticsearchClient
from core import Mapper
from db import redis
from models import Genre, Movie, Person

from .utils import SearchBodyCreator, backoff, cache, status


class BaseService(ABC):
    """An abstract service for executing business logic."""

    def __init__(self, client: AsyncElasticsearchClient, mapper: Mapper):
        """Initialization of service."""

        self.client = client
        self.mapper = mapper
        self.search_creator = SearchBodyCreator(self.mapper.search_body)

    @backoff((ElasticsearchConnectionError, RedisConnectionError))
    @cache(redis.storage, RedisConnectionError)
    @status()
    async def get_by_id(self, uuid: UUID) -> Genre | Movie | Person | None:
        """Get movie by id from Elasticsearch."""

        return await self.client.get_by_id(uuid, self.mapper)

    @backoff((ElasticsearchConnectionError, RedisConnectionError))
    @cache(redis.storage, RedisConnectionError)
    @status()
    async def search(
        self,
        query: str | None = None,
        sort_by: str | None = None,
        filter_by: tuple[str, str] | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Genre | Movie | Person] | None:
        """Full-text search of movies from movies database."""

        search_body = self.search_creator.create_search_body(query, sort_by, filter_by, (page, page_size))

        return await self.client.search(search_body, self.mapper)
