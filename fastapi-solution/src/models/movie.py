from pydantic import BaseModel, Field

from .genre import _Genre
from .mixin import OrjsonMixin, UUIDMixin
from .person import _Person


class _Movie(UUIDMixin):
    """Movie model with short description."""

    title: str = Field(example='1983 MLB All-Star Game')
    imdb_rating: float | None = Field(default=None, example=6.5)


class Movies(BaseModel):
    """Movie models with short description."""

    movies: list[_Movie] = Field(default_factory=list)


class MovieFull(_Movie):
    """Movie model with full description."""

    description: str | None = Field(default=None, example='Something interesting about movie')
    genres: list[_Genre] = Field(default_factory=list)
    actors: list[_Person] = Field(default_factory=list)
    directors: list[_Person] = Field(default_factory=list)
    writers: list[_Person] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list, example=['Kendrick Lamar'])
    writers_names: list[str] = Field(default_factory=list, example=['Kendrick Lamar'])


class Movie(MovieFull, OrjsonMixin):
    """Movie model for business logic."""

    pass
