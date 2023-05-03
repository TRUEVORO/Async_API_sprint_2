import time
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ElasticsearchConnectionError
from elasticsearch.helpers import bulk
from tests.functional.settings import test_settings
from tests.functional.utils.json_reader import read_index, read_test_data

BASE_DIR: Path = Path(__file__).resolve().parents[1]


def ping_elasticsearch(
    elasticsearch_client: Elasticsearch,
    start_sleep_time: float = 0.1,
    attempts: int = 10,
    factor: int = 2,
    border_sleep_time: int = 10,
) -> None:
    """Ping the Elasticsearch until it is available."""

    sleep_time = start_sleep_time

    for _ in range(attempts):
        if elasticsearch_client.ping():
            return

        sleep_time = min(sleep_time * 2**factor, border_sleep_time)
        time.sleep(sleep_time)

    raise ElasticsearchConnectionError(message='Elasticsearch is not available, please check if it is running')


if __name__ == '__main__':
    client = Elasticsearch(test_settings.elasticsearch_dsn)

    ping_elasticsearch(client)

    for index in ['genres', 'movies', 'persons']:
        if not client.indices.exists(index=index):
            client.indices.create(index=index, **read_index(index))

            test_data = read_test_data(index)

            for row in test_data[index]:
                row['_id'] = row['id']

            bulk(client, index=index, actions=test_data[index], chunk_size=test_data['total'])
