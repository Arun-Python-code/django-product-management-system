#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Load the project settings and pass command-line arguments to Django."""
    # Use the project's settings module unless the environment overrides it.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userApp.settings')
    try:
        # Import here so this script can provide a clearer error if Django is absent.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Only start the command-line runner when this file is executed directly.
    main()
