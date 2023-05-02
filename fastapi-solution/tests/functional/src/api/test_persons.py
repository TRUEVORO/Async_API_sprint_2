from uuid import uuid4

import pytest
from pydantic import AnyHttpUrl
from tests.functional.settings import test_settings
from tests.functional.test_data import PERSONS_DATA
from tests.functional.utils import PersonTest

PERSONS_URL: AnyHttpUrl = test_settings.service_dsn + '/api/v1/persons'

PERSONS_SHORT: list[dict] = [PersonTest(**row).dict() for row in PERSONS_DATA['persons']]


PERSONS_SORTED_BY_FULL_NAME_ASC: list[dict] = sorted(PERSONS_SHORT, key=lambda x: x['full_name'])
PERSONS_SORTED_BY_FULL_NAME_DESC: list[dict] = sorted(PERSONS_SHORT, key=lambda x: x['full_name'], reverse=True)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'person_id': PERSONS_DATA['persons'][0]['id']}, {'status': 200, 'body': PERSONS_DATA['persons'][0]}),
        ({'person_id': str(uuid4())}, {'status': 404, 'body': {'detail': 'not found'}}),
        (
            {'person_id': 'non-existent'},
            {
                'status': 422,
                'body': {
                    'detail': [
                        {'loc': ['path', 'person_id'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}
                    ]
                },
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_person_details(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the person details API endpoint."""

    body, status = await make_get_request(
        url='{}/<{}:UUID>/'.format(PERSONS_URL, query_data['person_id']), query_data=query_data
    )

    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_ASC[:50], 'length': 50},
        ),
        ({'sort': 'full_name'}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_ASC[:50], 'length': 50}),
        ({'sort': '-full_name'}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_DESC[:50], 'length': 50}),
        ({'sort': 'non-existent'}, {'status': 422, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': 200, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_ASC[:2], 'length': 2}),
    ],
)
@pytest.mark.asyncio
async def test_persons_main(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the main persons API endpoint."""

    body, status = await make_get_request(url=PERSONS_URL, query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('persons', []) == expected_answer['body']
    assert len(body.get('persons', [])) <= expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': PERSONS_DATA['persons'][0]['full_name'], 'page_size': 1},
            {'status': 200, 'body': [PersonTest(**PERSONS_DATA['persons'][0]).dict()], 'length': 1},
        ),
        ({'query': 'non-existent'}, {'status': 404, 'body': [], 'length': 0}),
        ({'sort': 'full_name'}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_ASC[:50], 'length': 50}),
        ({'sort': '-full_name'}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_DESC[:50], 'length': 50}),
        ({'sort': 'non-existent'}, {'status': 422, 'body': [], 'length': 0}),
        ({'page': 5}, {'status': 200, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 2}, {'status': 200, 'body': PERSONS_SORTED_BY_FULL_NAME_ASC[:2], 'length': 2}),
    ],
)
@pytest.mark.asyncio
async def test_persons_search(make_get_request, redis_clean_data, query_data, expected_answer):
    """Test the persons search API endpoint."""

    body, status = await make_get_request(url=f'{PERSONS_URL}/search', query_data=query_data)

    assert status == expected_answer['status']
    assert body.get('persons', []) == expected_answer['body']
    assert len(body.get('persons', [])) <= expected_answer['length']
