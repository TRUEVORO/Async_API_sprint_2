from pydantic import BaseModel, Field

from .mixin import OrjsonMixin, UUIDMixin


class _Films(UUIDMixin):
    """Films model with person's roles."""

    roles: list[str] = Field(default_factory=list)


class _Person(UUIDMixin):
    """Person model."""

    full_name: str = Field(default_factory=str)
    films: list[_Films] = Field(default_factory=list)


class Persons(BaseModel):
    """Person models."""

    persons: list[_Person] = Field(default_factory=list)


class Person(_Person, OrjsonMixin):
    """Person model for business logic."""

    pass
