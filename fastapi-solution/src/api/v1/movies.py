from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from models import MovieFull, Movies
from services import MovieService, get_movie_service

router = APIRouter(
    prefix='/api/v1/movies',
    tags=['movies'],
)


class MoviesAPI(Movies):
    """API model for list of movies."""

    total: int


class MovieAPIFull(MovieFull):
    """API model for movie with full description."""

    pass


@router.get(
    '/<{movie_id}:UUID>/',
    response_model=MovieAPIFull,
    summary='Search movie',
    description='Search movie by id',
    response_description='Full film details',
)
async def movie_detail(
    movie_id: Annotated[UUID, Path(title='movie id', description='parameter - movie id')],
    movie_service: MovieService = Depends(get_movie_service),
) -> MovieAPIFull | HTTPException:
    movie = await movie_service.get_by_id(uuid=movie_id)
    return MovieAPIFull(**movie.dict(by_alias=True))


@router.get(
    '',
    response_model=MoviesAPI,
    summary='Popular movies',
    description='Popular movies with sorting and filtering by genre',
    response_description='Summary of movies',
)
async def movies_main(
    sort: Annotated[
        Literal['title', '-title', 'imdb_rating', '-imdb_rating'] | None,
        Query(title='sort', description='optional parameter - sort'),
    ] = None,
    genre: Annotated[str | None, Query(title='genre', description='optional parameter - filter by genre')] = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    movie_service: MovieService = Depends(get_movie_service),
) -> MoviesAPI | HTTPException:
    movies, total = await movie_service.search(
        sort_by=sort, filter_by=('genres', genre) if genre else None, page=page, page_size=page_size
    )
    return MoviesAPI(movies=movies, total=total)


@router.get(
    '/search',
    response_model=MoviesAPI,
    summary='Search movies',
    description='Full-text search of movies with sorting and filtering by genre',
    response_description='Summary of movies',
)
async def movies_search(
    query: Annotated[str | None, Query(title='query', description='optional parameter - query')] = None,
    sort: Annotated[
        Literal['title', '-title', 'imdb_rating', '-imdb_rating'] | None,
        Query(title='sort', description='optional parameter - sort'),
    ] = None,
    genre: Annotated[str | None, Query(title='genre', description='optional parameter - filter by genre')] = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    movie_service: MovieService = Depends(get_movie_service),
) -> MoviesAPI | HTTPException:
    movies, total = await movie_service.search(
        query=query, sort_by=sort, filter_by=('genres', genre) if genre else None, page=page, page_size=page_size
    )
    return MoviesAPI(movies=movies, total=total)
