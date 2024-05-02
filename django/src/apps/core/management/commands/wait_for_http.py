"""Django management command ``wait_for_http``"""

from typing import Self

import backoff
import requests
from django.core.management.base import BaseCommand, CommandError, CommandParser


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ),
    max_time=60,
)
def run_request(url: str) -> None:
    response = requests.get(url=url, timeout=60)
    response.raise_for_status()


def wait_for_http(**opts) -> None:  # noqa: ANN003
    """The main loop waiting for the http connection to come up."""
    url = opts["url"]
    run_request(url=url)
    print("Connection successfull")


class Command(BaseCommand):
    """A readiness probe you can use for Kubernetes.

    If the service is ready, i.e. willing to accept connections
    and handling requests, then this call will exit successfully. Otherwise
    the command exits with an error status after reaching a timeout.
    """

    help = "Probes for http service availability"

    def add_arguments(self: Self, parser: CommandParser) -> None:
        parser.add_argument("url", type=str, help="HTTP Healthcheck endpoint")
        parser.add_argument(
            "--timeout",
            "-t",
            type=int,
            default=180,
            metavar="SECONDS",
            action="store",
            help="how long to wait for the http service"
            + "before timing out (seconds), default: 180",
        )
        parser.add_argument(
            "--stable",
            "-s",
            type=int,
            default=5,
            metavar="SECONDS",
            action="store",
            help="how long to observe whether connection"
            + "is stable (seconds), default: 5",
        )
        parser.add_argument(
            "--wait-when-down",
            "-d",
            type=int,
            default=2,
            metavar="SECONDS",
            action="store",
            help="delay between checks when http service is down (seconds), default: 2",
        )
        parser.add_argument(
            "--wait-when-alive",
            "-a",
            type=int,
            default=1,
            metavar="SECONDS",
            action="store",
            help="delay between checks when http service is up (seconds), default: 1",
        )

    def handle(self: Self, **options) -> None:  # noqa: ANN003
        """Wait for a http connection to come up. Exit with error
        status when a timeout threshold is surpassed.
        """
        try:
            wait_for_http(**options)
        except TimeoutError as err:
            raise CommandError(err) from err
