"""
ASGI config for userApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Select the settings module used by ASGI application servers.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userApp.settings')

# Expose Django's ASGI callable to the deployment server.
application = get_asgi_application()
