# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys

from django.core.wsgi import get_wsgi_application


# python
sys.path.append('/d2/python_venv/3.10/djforms/lib/python3.10/')
sys.path.append('/d2/python_venv/3.10/djforms/lib/python3.10/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djforms.settings.shell')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# wsgi
application = get_wsgi_application()
