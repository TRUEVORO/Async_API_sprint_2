from copy import deepcopy


class SearchBodyCreator:
    """Class creator of Elasticsearch search body."""

    def __init__(self, search_body: dict):
        """Initialization of SearchBodyCreator."""

        self.search_body = search_body

    def query(self, query: str | None = None, search_body: dict | None = None) -> dict:
        """
        Add query to Elasticsearch search body.

        :param query: enquiry text
        :param search_body: search body for Elasticsearch
        :return: search body with specific query
        """

        if not isinstance(search_body, dict):
            search_body = deepcopy(self.search_body)

        if query:
            search_body['query']['multi_match']['query'] = query
        else:
            search_body['query'] = {'match_all': {}}

        return search_body

    def sort(self, key: str, search_body: dict) -> dict:
        """
        Add sort to Elasticsearch search body.

        :param key: key to sort
        :param search_body: search body for Elasticsearch
        :return: search body with sorting by specific key
        """

        if not isinstance(search_body, dict):
            search_body = deepcopy(self.search_body)

        if key[0] == '-':
            key = key[1:]
            order = 'desc'
        else:
            order = 'asc'

        if key != 'imdb_rating':
            key = f'{key}.raw'

        search_body['sort'][0] = {key: {'order': order}}

        return search_body

    def filter(self, key: str, value: str, search_body: dict | None = None) -> dict:
        """
        Add filter to Elasticsearch search body.

        :param key: filter key
        :param value: value for filtering
        :param search_body: search body for Elasticsearch
        :return: search body with filtering by specific key and value
        """

        if not isinstance(search_body, dict):
            search_body = deepcopy(self.search_body)

        match = search_body.pop('query')
        search_body['query'] = {
            'bool': {
                'must': match,
                'filter': [
                    {
                        'nested': {
                            'path': key,
                            'query': {
                                'match': {f'{key}.name': value},
                            },
                        },
                    },
                ],
            },
        }

        return search_body

    def paginate(self, page: int, page_size: int, search_body: dict | None = None) -> dict:
        """
        Add pagination to Elasticsearch search body.

        :param page: page number
        :param page_size: content size on the page
        :param search_body: search body for Elasticsearch
        :return: search body with pagination
        """

        if not isinstance(search_body, dict):
            search_body = deepcopy(self.search_body)

        search_body['from'] = page - 1
        search_body['size'] = page_size

        return search_body

    def create_search_body(
        self,
        query: str | None = None,
        sort_by: str | None = None,
        filter_by: tuple[str, str] | None = None,
        pagination: tuple[int, int] = (1, 50),
    ) -> dict:
        """
        Create Elasticsearch search body with specific parameters.

        :param query: enquiry text
        :param sort_by: sorting parameter
        :param filter_by: filtering parameters
        :param pagination: pagination parameters
        :return: Elasticsearch search body with specific parameters
        """

        search_body = self.query(query)

        search_body = self.paginate(*pagination, search_body=search_body)

        if sort_by:
            search_body = self.sort(sort_by, search_body)

        if filter_by:
            search_body = self.filter(filter_by[0], filter_by[1], search_body)

        return search_body
