import logging

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import genres_router, movies_router, persons_router
from client import AsyncElasticsearchClient
from core import LOGGING, security_jwt_remote, settings
from db import elasticsearch, redis

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Information about movies, genres, and people involved in creating the film work',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    elasticsearch.elasticsearch = AsyncElasticsearchClient(AsyncElasticsearch(settings.elasticsearch_dsn))


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elasticsearch.elasticsearch.close()


app.include_router(
    movies_router,
    dependencies=[Depends(security_jwt_remote)],
)
app.include_router(
    genres_router,
    dependencies=[Depends(security_jwt_remote)],
)
app.include_router(
    persons_router,
    dependencies=[Depends(security_jwt_remote)],
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
