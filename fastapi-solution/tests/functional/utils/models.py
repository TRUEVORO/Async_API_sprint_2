from pydantic import BaseModel, Field


class MovieTest(BaseModel):
    """Movie model for tests."""

    id: str
    title: str
    imdb_rating: float | None = Field(default=None)


class PersonTest(BaseModel):
    """Person model for tests."""

    id: str
    full_name: str
