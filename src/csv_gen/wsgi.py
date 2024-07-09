"""
WSGI config for csv_gen project.

This module configures the WSGI application for the Django project to serve in production environments.
It sets the Django settings module to use the production settings file.

For more information on this file, see:
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Point to the production settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_gen.settings_prod')

application = get_wsgi_application()
