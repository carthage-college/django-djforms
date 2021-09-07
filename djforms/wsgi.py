# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys

from django.core.wsgi import get_wsgi_application


# python
sys.path.append('/d2/python_venv/3.6/djforms/lib/python3.6/')
sys.path.append('/d2/python_venv/3.6/djforms/lib/python3.6/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djforms.settings.staging')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# wsgi
application = get_wsgi_application()
