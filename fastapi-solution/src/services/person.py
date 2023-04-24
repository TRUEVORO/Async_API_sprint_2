from functools import lru_cache

from fastapi import Depends

from client import AsyncElasticsearchClient
from core import Mapper
from db import get_elastic
from models import Person

from .base_service import BaseService
from .utils import SearchTemplates


class PersonService(BaseService):
    """Person class for executing business logic."""

    def __init__(self, client: AsyncElasticsearchClient):
        """Initialization of person service."""

        super().__init__(client, Mapper('persons', Person, SearchTemplates().PERSON_TEMPLATE))


@lru_cache
def get_person_service(
    elasticsearch: AsyncElasticsearchClient = Depends(get_elastic),
) -> PersonService:
    return PersonService(elasticsearch)
