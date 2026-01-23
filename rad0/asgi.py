"""
ASGI config for rad0 project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rad0.settings')

application = get_asgi_application()
