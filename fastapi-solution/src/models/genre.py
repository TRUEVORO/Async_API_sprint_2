from pydantic import BaseModel, Field

from .mixin import OrjsonMixin, UUIDMixin


class _Genre(UUIDMixin):
    """Genre model."""

    name: str = Field(default_factory=str)


class Genres(BaseModel):
    """Genre models."""

    genres: list[_Genre] = Field(default_factory=list)


class Genre(_Genre, OrjsonMixin):
    """Genre model for business logic."""

    pass
