from http import HTTPStatus
from uuid import uuid4

import pytest
from pydantic import AnyHttpUrl
from tests.functional.settings import test_settings
from tests.functional.test_data import GENRES_DATA, MOVIES_DATA
from tests.functional.utils import MovieTest

pytestmark = pytest.mark.asyncio

MOVIES_URL: AnyHttpUrl = test_settings.service_dsn + '/api/v1/movies'

MOVIES_SHORT: list[dict] = [MovieTest(**row).dict() for row in MOVIES_DATA['movies']]

MOVIES_SORTED_BY_TITLE_ASC: list[dict] = sorted(MOVIES_SHORT, key=lambda x: x['title'])
MOVIES_SORTED_BY_TITLE_DESC: list[dict] = sorted(MOVIES_SHORT, key=lambda x: x['title'], reverse=True)
MOVIES_SORTED_BY_IMDB_RATING_ASC: list[dict] = sorted(MOVIES_SHORT, key=lambda x: x['imdb_rating'])
MOVIES_SORTED_BY_IMDB_RATING_DESC: list[dict] = sorted(MOVIES_SHORT, key=lambda x: x['imdb_rating'], reverse=True)

MOVIES_FILTER_BY_GENRE = [
    MovieTest(**row).dict()
    for row in MOVIES_DATA['movies']
    if GENRES_DATA['genres'][0]['name'] in [genre['name'] for genre in row['genres']]
]


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'movie_id': MOVIES_DATA['movies'][0]['id']}, {'status': HTTPStatus.OK, 'body': MOVIES_DATA['movies'][0]}),
        ({'movie_id': str(uuid4())}, {'status': HTTPStatus.NOT_FOUND, 'body': {'detail': 'not found'}}),
        (
            {'movie_id': 'non-existent'},
            {
                'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                'body': {
                    'detail': [
                        {'loc': ['path', 'movie_id'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}
                    ]
                },
            },
        ),
    ],
)
async def test_movie_details(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the movie details API endpoint."""

    body, status = await make_get_request(
        url='{}/<{}:UUID>/'.format(MOVIES_URL, query_data['movie_id']), query_data=query_data
    )

    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_ASC[:50], 'length': 50},
        ),
        ({'sort': 'title'}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_ASC[:50], 'length': 50}),
        ({'sort': '-title'}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_DESC[:50], 'length': 50}),
        (
            {'sort': 'imdb_rating'},
            {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_IMDB_RATING_ASC[:50], 'length': 50},
        ),
        (
            {'sort': '-imdb_rating'},
            {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_IMDB_RATING_DESC[:50], 'length': 50},
        ),
        ({'sort': 'non-existent'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'body': [], 'length': 0}),
        (
            {'genre': GENRES_DATA['genres'][0]['name']},
            {'status': HTTPStatus.OK, 'body': MOVIES_FILTER_BY_GENRE[:50], 'length': 50},
        ),
        ({'genre': 'non-existent'}, {'status': HTTPStatus.NOT_FOUND, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': HTTPStatus.OK, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_ASC[:2], 'length': 2}),
    ],
)
async def test_movies_main(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the main movies API endpoint."""

    body, status = await make_get_request(url=MOVIES_URL, query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('movies', []) == expected_answer['body']
    assert len(body.get('movies', [])) <= expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': MOVIES_DATA['movies'][0]['title'], 'page_size': 1},
            {'status': HTTPStatus.OK, 'body': [MovieTest(**MOVIES_DATA['movies'][0]).dict()], 'length': 1},
        ),
        ({'query': 'non-existent'}, {'status': HTTPStatus.NOT_FOUND, 'body': [], 'length': 0}),
        ({'sort': 'title'}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_ASC[:50], 'length': 50}),
        ({'sort': '-title'}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_DESC[:50], 'length': 50}),
        (
            {'sort': 'imdb_rating'},
            {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_IMDB_RATING_ASC[:50], 'length': 50},
        ),
        (
            {'sort': '-imdb_rating'},
            {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_IMDB_RATING_DESC[:50], 'length': 50},
        ),
        ({'sort': 'non-existent'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'body': [], 'length': 0}),
        (
            {'genre': GENRES_DATA['genres'][0]['name']},
            {'status': HTTPStatus.OK, 'body': MOVIES_FILTER_BY_GENRE[:50], 'length': 50},
        ),
        ({'genre': 'non-existent'}, {'status': HTTPStatus.NOT_FOUND, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': HTTPStatus.OK, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': HTTPStatus.OK, 'body': MOVIES_SORTED_BY_TITLE_ASC[:2], 'length': 2}),
    ],
)
async def test_movies_search(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the movies search API endpoint."""

    body, status = await make_get_request(url=f'{MOVIES_URL}/search', query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('movies', []) == expected_answer['body']
    assert len(body.get('movies', [])) <= expected_answer['length']
