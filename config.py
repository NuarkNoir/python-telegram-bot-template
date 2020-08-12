# This module contains config class


class Config:
    TOKEN = ""  # Token of your bot
    LIST_OF_ADMINS = []  # List of administrators. Decorator @restricted uses this list to chek if user admin

    LOG_LEVEL = 10  # 10 == logging.DEBUG
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    DB_FILENAME = ":memory:"  # If you are using sqlite, then change it to your desired DB filename
