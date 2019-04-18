import logging
import sys
import time
from functools import wraps

logger = logging.getLogger('bot')


def retry(exceptions, max_tries=4, delay=5, backoff=1.5, log_on_failure=None, fatal=False):
    def deco_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            tries, current_delay = 0, delay
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    tries += 1
                    logger.error(
                        "Retried {0.__name__} for time {1}/{2}. "
                        "{3.__class__.__name__}: {3}".format(func, tries, max_tries, e))
                    current_delay *= backoff
                    time.sleep(current_delay)

            if log_on_failure:
                logger.error(log_on_failure)
            else:
                logger.error(
                    "{0.__name__} failed {1} time(s).".format(func, tries))
            if fatal:
                sys.exit()
            else:
                return func(*args, **kwargs)
        return func_retry
    return deco_retry
