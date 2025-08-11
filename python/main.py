#!/usr/bin/env python3

"""Main script."""

import logging
import pathlib

import environ

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))

logger = logging.getLogger(__name__)


def start() -> None:
    """Start the application."""
    logger.debug("only printed in DEBUG")
    logger.info("hello world!")


if __name__ == "__main__":
    start()
