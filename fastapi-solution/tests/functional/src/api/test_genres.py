from http import HTTPStatus
from uuid import uuid4

import pytest
from pydantic import AnyHttpUrl
from tests.functional.settings import test_settings
from tests.functional.test_data import GENRES_DATA

pytestmark = pytest.mark.asyncio

GENRES_URL: AnyHttpUrl = test_settings.service_dsn + '/api/v1/genres'
GENRES_SORTED_BY_NAME_ASC: list[dict] = sorted(GENRES_DATA['genres'], key=lambda x: x['name'])
GENRES_SORTED_BY_NAME_DESC: list[dict] = sorted(GENRES_DATA['genres'], key=lambda x: x['name'], reverse=True)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'genre_id': GENRES_DATA['genres'][0]['id']}, {'status': HTTPStatus.OK, 'body': GENRES_DATA['genres'][0]}),
        ({'genre_id': str(uuid4())}, {'status': HTTPStatus.NOT_FOUND, 'body': {'detail': 'not found'}}),
        (
            {'genre_id': 'non-existent'},
            {
                'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                'body': {
                    'detail': [
                        {'loc': ['path', 'genre_id'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}
                    ]
                },
            },
        ),
    ],
)
async def test_genre_details(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the genre details API endpoint."""

    body, status = await make_get_request(
        url='{}/<{}:UUID>/'.format(GENRES_URL, query_data['genre_id']), query_data=query_data
    )

    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_ASC[:50], 'length': 50},
        ),
        ({'sort': 'name'}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_ASC[:50], 'length': 50}),
        ({'sort': '-name'}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_DESC[:50], 'length': 50}),
        ({'sort': 'non-existent'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': HTTPStatus.OK, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_ASC[:2], 'length': 2}),
    ],
)
async def test_genres_main(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the main genres API endpoint."""

    body, status = await make_get_request(url=GENRES_URL, query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('genres', []) == expected_answer['body']
    assert len(body.get('genres', [])) <= expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': GENRES_DATA['genres'][0]['name']},
            {'status': HTTPStatus.OK, 'body': GENRES_DATA['genres'][:1], 'length': 1},
        ),
        ({'query': 'non-existent'}, {'status': HTTPStatus.NOT_FOUND, 'body': [], 'length': 0}),
        ({'sort': 'name'}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_ASC[:50], 'length': 50}),
        ({'sort': '-name'}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_DESC[:50], 'length': 50}),
        ({'sort': 'non-existent'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': HTTPStatus.OK, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': HTTPStatus.OK, 'body': GENRES_SORTED_BY_NAME_ASC[:2], 'length': 2}),
    ],
)
async def test_genres_search(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the genres search API endpoint."""

    body, status = await make_get_request(url=f'{GENRES_URL}/search', query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('genres', []) == expected_answer['body']
    assert len(body.get('genres', [])) <= expected_answer['length']
