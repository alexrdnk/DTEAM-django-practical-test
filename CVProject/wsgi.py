"""
WSGI config for CVProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

# Use production settings if in production environment
if config('DEBUG', default=True, cast=bool) == False:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings')

application = get_wsgi_application()
