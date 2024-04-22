import logging

import environ

env = environ.Env()
DEBUG = env("DEBUG", default=False)


def start() -> None:
    if DEBUG:
        logging.debug("Debug mode active")

    print("hello world!")


if __name__ == "__main__":
    start()
