import time
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tests.functional.settings import test_settings
from tests.functional.utils.json_reader import read_index, read_test_data

BASE_DIR: Path = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    client = Elasticsearch(test_settings.elasticsearch_dsn)

    while True:
        if client.ping():
            break
        time.sleep(1)

    for index in ['genres', 'movies', 'persons']:
        if not client.indices.exists(index=index):
            client.indices.create(index=index, **read_index(index))

            test_data = read_test_data(index)

            for row in test_data[index]:
                row['_id'] = row['id']

            bulk(client, index=index, actions=test_data[index], chunk_size=test_data['total'])
