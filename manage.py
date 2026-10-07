#!/usr/bin/env python
"""Командная утилита Django-проекта."""
import os
import sys


def main() -> None:
    """Запустить административную команду Django."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "equipment_service.settings",
    )
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
