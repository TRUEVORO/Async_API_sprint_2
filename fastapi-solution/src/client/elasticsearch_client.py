from uuid import UUID

from elasticsearch import NotFoundError

from core import Mapper
from models import Genre, Movie, Person

from .base_client import AsyncBaseClient


class AsyncElasticsearchClient(AsyncBaseClient):
    """An async Elasticsearch client to retrieve data."""

    async def get_by_id(self, uuid: UUID, mapper: Mapper) -> Genre | Movie | Person | None:
        """Get data by id from Elasticsearch."""

        try:
            doc = await self.connection.get(index=mapper.index, id=str(uuid))
        except NotFoundError:
            return None

        return mapper.model(**doc['_source'])

    async def search(self, search_body: dict, mapper: Mapper) -> tuple[list[Genre | Movie | Person], int] | None:
        """Search data in Elasticsearch."""

        try:
            docs = await self.connection.search(index=mapper.index, body=search_body)
        except NotFoundError:
            return None

        return [mapper.model(**doc['_source']) for doc in docs['hits']['hits']], docs['hits']['total']['value']
