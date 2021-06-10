"""
WSGI config for mySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
    sys.path.append(path)

application = get_wsgi_application()
