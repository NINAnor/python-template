#!/usr/bin/env python
import os
import sys
from pathlib import Path


def django_manage() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError as e:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?",
            ) from e

        raise

    # This allows easy placement of apps within the interior
    # apps directory.
    current_path = Path(__file__).parent.parent.resolve()
    sys.path.append(str(current_path / "apps"))

    execute_from_command_line(sys.argv)
