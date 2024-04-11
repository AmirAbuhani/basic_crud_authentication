import logging
from fastapi import HTTPException, Body

from models.users_model import UserSchema

logger = logging.getLogger(__name__)


def log_authentication(func):
    def wrapper(user: UserSchema = Body(default=None)):
        username = user.username
        logger.info(f"Authentication request received for user: {username}")
        return func(user)

    return wrapper


def log_request(func):
    def wrapper():
        logger.info(f"Request made to {func.__name__} endpoint")
        return func()

    return wrapper


def log_success(func):
    def wrapper():
        result = func()
        logger.info(f"Operation successful: {func.__name__}")
        return result

    return wrapper


def log_error(func):
    def wrapper():
        try:
            return func()
        except Exception as e:
            logger.error(f"Error encountered in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper
