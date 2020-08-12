# This is entry point of your bot
from config import Config
import logging
import bot_frame
import atexit

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def main():
    bot_frame.run()


@atexit.register
def _stop_worker_threads():
    bot_frame.stop()


if __name__ == "__main__":
    main()
