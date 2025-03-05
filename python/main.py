import logging
import pathlib

import environ

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))


def start() -> None:
    logging.debug("only printed in DEBUG")
    print("hello world!")


if __name__ == "__main__":
    start()
