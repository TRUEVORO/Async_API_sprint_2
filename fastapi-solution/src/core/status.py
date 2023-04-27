from functools import wraps
from http import HTTPStatus

from elasticsearch import ConnectionError
from fastapi import HTTPException


def status():
    """
    Function for retrieving status of request.

    :return: results of the search or HTTPException
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
            except ConnectionError:
                raise HTTPException(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail='client is unavailable, retry later'
                )

            if not result:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='not found')

            return result

        return inner

    return func_wrapper
