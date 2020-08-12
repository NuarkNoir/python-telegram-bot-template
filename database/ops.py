# This module contains operations you may need to interact with DB
# Simply put there functions like add/get user
from peewee import DoesNotExist
from database.db import User


def get_user(tg_user_id: int) -> (User, None):
    try:
        return User.get(User.tg_user_id == tg_user_id)
    except DoesNotExist:
        return None


def add_user(tg_user_id: int, tg_first_name: str, tg_last_name: str = "", tg_username: str = "") -> User:
    user = User(
        tg_user_id=tg_user_id,
        tg_first_name=tg_first_name,
        tg_last_name=tg_last_name,
        tg_username=tg_username,
    )
    user.save()
    return user
