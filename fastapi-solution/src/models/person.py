from pydantic import BaseModel, Field

from .mixin import OrjsonMixin, UUIDMixin


class _Films(UUIDMixin):
    """Films model with person's roles."""

    roles: list[str] = Field(default_factory=list, example=['actor', 'director', 'writer'])


class _Person(UUIDMixin):
    """Person model."""

    full_name: str = Field(default_factory=str, example='Kendrick Lamar')


class PersonFull(_Person):
    """Person model with films."""

    films: list[_Films] = Field(default_factory=list)


class Persons(BaseModel):
    """Persons model."""

    persons: list[_Person] = Field(default_factory=list)


class Person(PersonFull, OrjsonMixin):
    """Person model for business logic."""

    pass
