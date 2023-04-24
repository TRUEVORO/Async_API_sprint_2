from functools import lru_cache

from fastapi import Depends

from client import AsyncElasticsearchClient
from core import Mapper
from db import get_elastic
from models import Movie

from .base_service import BaseService
from .utils import SearchTemplates


class MovieService(BaseService):
    """Movie class for executing business logic."""

    def __init__(self, client: AsyncElasticsearchClient):
        """Initialization of movie service."""

        super().__init__(client, Mapper('movies', Movie, SearchTemplates().MOVIE_TEMPLATE))


@lru_cache
def get_movie_service(
    elasticsearch: AsyncElasticsearchClient = Depends(get_elastic),
) -> MovieService:
    return MovieService(elasticsearch)
