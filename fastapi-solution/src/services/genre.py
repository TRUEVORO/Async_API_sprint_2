from functools import lru_cache

from fastapi import Depends

from client import AsyncElasticsearchClient
from core import Mapper
from db import get_elastic
from models import Genre

from .base_service import BaseService
from .utils import SearchTemplates


class GenreService(BaseService):
    """Genre class for executing business logic."""

    def __init__(self, client: AsyncElasticsearchClient):
        """Initialization of genre service."""

        super().__init__(client, Mapper('genres', Genre, SearchTemplates().GENRE_TEMPLATE))


@lru_cache
def get_genre_service(
    elasticsearch: AsyncElasticsearchClient = Depends(get_elastic),
) -> GenreService:
    return GenreService(elasticsearch)
