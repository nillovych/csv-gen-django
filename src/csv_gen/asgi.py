"""
ASGI config for csv_gen project.

This module configures ASGI application for use with Django, enabling asynchronous web functionality.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'csv_gen' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_gen.settings_prod')

# Get the ASGI application for Django.
application = get_asgi_application()