import os, sys

#Add the path to 3rd party django application and to django itself.

sys.path.append('/usr/lib/python2.5/site-packages/')
sys.path.append('/usr/lib/python2.5/')
sys.path.append('/data2/django_src/')
sys.path.append('/data2/django_projects/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'djforms.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
# for TZ see:
# http://groups.google.com/group/django-users/browse_thread/thread/c75ad3d36dda5d78?hl=en
os.environ['TZ']='America/Chicago'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
