from functools import wraps

from core import NotFoundServiceError


def status():
    """
    Function for retrieving status of request.

    :return: results of the search or HTTPException
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            result = await func(*args, **kwargs)

            if not result or 0 in result:
                raise NotFoundServiceError()

            return result

        return inner

    return func_wrapper
