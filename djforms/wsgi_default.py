import os, sys
# python
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.5.5/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
# django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djforms.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
os.environ['TZ']='America/Chicago'
# wsgi
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
