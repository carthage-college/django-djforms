import os, sys

#Add the path to 3rd party django application and to django itself.

sys.path.append('/usr/lib/python2.6/site-packages/')
sys.path.append('/usr/lib/python2.6/')
sys.path.append('/data2/django_trunk/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_projects/sputnik/production/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'djforms.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/python/.python-eggs'
os.environ['TZ']='America/Chicago'
# informix
os.environ['INFORMIXSERVER'] = 'wilson'
os.environ['INFORMIXDIR'] = '/opt/ibm/informix'
os.environ['LD_LIBRARY_PATH'] = '$INFORMIXDIR/lib:$INFORMIXDIR/lib/esql:$INFORMIXDIR/lib/tools:/usr/lib/apache2/modules:$INFORMIXDIR/lib/cli'
os.environ['LD_RUN_PATH'] = '/opt/ibm/informix/lib:/opt/ibm/informix/lib/esql:/opt/ibm/informix/lib/tools:/usr/lib/apache2/modules'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
