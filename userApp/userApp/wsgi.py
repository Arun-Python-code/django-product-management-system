"""
WSGI config for userApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Select the settings module used by WSGI application servers.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userApp.settings')

# Expose Django's WSGI callable to the deployment server.
application = get_wsgi_application()
