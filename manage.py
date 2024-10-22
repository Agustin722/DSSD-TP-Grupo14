#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings
from my_project import settings as mi_config

def establecer_datos_por_default():
    settings.configure(mi_config)
    from django.db import connection

    # Establece los datos por default
    cursor = connection.cursor()
    cursor.execute("INSERT INTO my_app_recolector (dni, password) VALUES ('12345678', '1234')")

def main():
    """Run administrative tasks."""
    if len(sys.argv) > 1 and sys.argv[1] == 'establecer_datos_por_default':
        establecer_datos_por_default()
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
