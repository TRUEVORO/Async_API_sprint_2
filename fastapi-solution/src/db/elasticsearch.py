from client import AsyncElasticsearchClient

elasticsearch: AsyncElasticsearchClient | None = None


async def get_elastic() -> AsyncElasticsearchClient:
    return elasticsearch
