import json
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parents[1]


def _read_json(file_path: str) -> dict:
    """Read data from json file."""

    with open(BASE_DIR / file_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)

    return data


def read_index(index: str) -> dict:
    """Read Elasticsearch index from json file."""

    return _read_json('utils/elasticsearch_indexes/{}.json'.format(index))


def read_test_data(index: str) -> dict[str, list | int]:
    """Read test data from specific json file."""

    return _read_json('test_data/json_data/{}.json'.format(index))
