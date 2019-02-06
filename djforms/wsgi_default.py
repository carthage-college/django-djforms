import os
import time
import traceback
import signal
import sys

# python
sys.path.append('/data2/python_venv/2.7/djforms/lib/python2.7/')
sys.path.append('/data2/python_venv/2.7/djforms/lib/python2.7/site-packages/')
sys.path.append('/data2/python_venv/2.7/djforms/lib/django_projects/')
sys.path.append('/data2/python_venv/2.7/djforms/lib/django-djforms/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djforms.settings')
os.environ.setdefault('PYTHON_EGG_CACHE', '')
os.environ.setdefault('TZ', 'America/Chicago')
# wsgi
from django.core.wsgi import get_wsgi_application

# NOTE: remove the try/except in production
#application = get_wsgi_application()
try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
    exit(-1)
