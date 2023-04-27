from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    """Mixin uuid model."""

    uuid: UUID = Field(default_factory=uuid4, alias='id')


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(BaseModel):
    """Model for fast json handling."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
