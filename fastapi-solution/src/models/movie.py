from pydantic import BaseModel, Field

from .genre import _Genre
from .mixin import OrjsonMixin, UUIDMixin
from .person import _Person


class _Movie(UUIDMixin):
    """Movie model with short description."""

    title: str
    imdb_rating: float | None = Field(default=None)


class Movies(BaseModel):
    """Movie models with short description."""

    movies: list[_Movie] = Field(default_factory=list)


class MovieFull(_Movie):
    """Movie model with full description."""

    description: str | None = Field(default=None)
    genres: list[_Genre] = Field(default_factory=list)
    actors: list[_Person] = Field(default_factory=list)
    directors: list[_Person] = Field(default_factory=list)
    writers: list[_Person] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)


class Movie(MovieFull, OrjsonMixin):
    """Movie model for business logic."""

    pass
