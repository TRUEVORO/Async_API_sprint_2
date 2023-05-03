import logging
import pickle
from functools import wraps
from logging import config as logging_config

from core import LOGGING
from storage import AsyncBaseStorage

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING)


def cache(storage: AsyncBaseStorage, connection_error: type[Exception], cache_lifetime: int = 300):
    """
    Function for working with cache from specific storage.
    It will store the data in storage if it was not there, and retrieve it from storage if it was there.

    :param storage: cache storage
    :param connection_error: storage connection error
    :param cache_lifetime: cache lifetime in seconds
    :return: data from cache or from function execution
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            key = '{0}_{1}_{2}'.format(func.__name__, args, kwargs)

            try:
                if data := await storage.retrieve_data(key):
                    return pickle.loads(data)
            except connection_error:  # noqa
                logger.exception('Cache storage connection error, cannot retrieve data from storage')

            if data := await func(*args, **kwargs):
                try:
                    await storage.save_data(key, pickle.dumps(data), cache_lifetime)
                except connection_error:  # noqa
                    logger.exception('Cache storage connection error, cannot save data to storage')

                return data

        return inner

    return func_wrapper
