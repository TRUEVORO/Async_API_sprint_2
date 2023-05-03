import asyncio
import logging
from functools import wraps
from logging import config as logging_config

from core import LOGGING, UnavailableServiceError

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING)


def backoff(
    expected_exceptions: tuple[type[Exception], ...],
    attempts: int = 1,
    start_sleep_time: float = 0.05,
    factor: int = 2,
    border_sleep_time: int = 10,
):
    """
    Function for retrying the execution of a function after some time if an error occurs.
    Uses a naive exponential growth of the retry time (factor) up to the maximum waiting time (border_sleep_time).

    Formula:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    :param expected_exceptions: expected exceptions to backoff
    :param attempts: number of attempts
    :param start_sleep_time: initial retry time
    :param factor: how many times to increase the waiting time
    :param border_sleep_time: maximum waiting time

    :return: the result of the function execution.
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            for _ in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except expected_exceptions:
                    sleep_time = min(sleep_time * 2**factor, border_sleep_time)
                    # logger.exception('Connection error, retrying in %s s', sleep_time)
                    await asyncio.sleep(sleep_time)

            raise UnavailableServiceError()

        return inner

    return func_wrapper
