import os, sys

#Add the path to 3rd party django application and to django itself.

sys.path.append('/usr/local/lib/python2.6/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_trunk/')
sys.path.append('/data2/django_projects/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'djforms.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
os.environ['TZ']='America/Chicago'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
