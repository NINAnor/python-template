import logging

import environ

logging.basicConfig()
env = environ.Env()
logging.getLogger().setLevel(env("LOG_LEVEL", default="INFO"))


def start() -> None:
    logging.debug("only printed with LOG_LEVEL=DEBUG")
    print("hello world!")


if __name__ == "__main__":
    start()
