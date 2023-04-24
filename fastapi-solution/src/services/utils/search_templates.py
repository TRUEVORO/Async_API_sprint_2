class SearchTemplates:
    """Class with search body templates for Elasticsearch."""

    @property
    def GENRE_TEMPLATE(self) -> dict:  # noqa
        """Search body template for searching genre in Elasticsearch."""

        return {
            'query': {
                'multi_match': {
                    'query': '*',
                    'fields': ['name'],
                },
            },
            'sort': [
                {'name.raw': {'order': 'asc'}},
            ],
        }

    @property
    def MOVIE_TEMPLATE(self) -> dict:  # noqa
        """Search body template for searching movie in Elasticsearch."""

        return {
            'query': {
                'multi_match': {
                    'query': '*',
                    'fields': [
                        'title^3',
                        'description',
                    ],
                },
            },
            'sort': [
                {'title.raw': {'order': 'asc'}},
            ],
        }

    @property
    def PERSON_TEMPLATE(self) -> dict:  # noqa
        """Search body template for searching person in Elasticsearch."""

        return {
            'query': {
                'multi_match': {
                    'query': '*',
                    'fields': ['full_name'],
                },
            },
            'sort': [
                {'full_name.raw': {'order': 'asc'}},
            ],
        }
