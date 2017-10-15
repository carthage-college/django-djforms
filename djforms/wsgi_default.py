import os
import time
import traceback
import signal
import sys

# python
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
#sys.path.append('/data2/django_1.5.5/')
#sys.path.append('/data2/django_1.6/')
sys.path.append('/data2/django_1.8/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
# django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djforms.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
os.environ['TZ']='America/Chicago'
# wsgi
from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
    exit(-1)
