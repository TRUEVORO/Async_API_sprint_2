from dataclasses import dataclass
from typing import Literal

from models import Genre, Movie, Person


@dataclass
class Mapper:
    """Model for describing each service."""

    index: Literal['genres', 'movies', 'persons']
    model: type(Movie) | type(Genre) | type(Person)
    search_body: dict
