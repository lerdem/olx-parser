import logging
from functools import wraps


logger = logging.getLogger('upload-logger')
handler = logging.FileHandler('cron-upload_ads-logs.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def log_function_call(func):
    """
    A decorator that logs the entry and exit of a function,
    including its arguments and return value.
    """
    @wraps(func)  # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"Entering function: {func_name} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting function: {func_name} with return value: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in function: {func_name} - {e}")
            raise  # Re-raise the exception after logging
    return wrapper
