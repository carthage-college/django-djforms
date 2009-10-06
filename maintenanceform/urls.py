from django.conf.urls.defaults import *
from djforms.maintenanceform.views import *

urlpatterns = patterns('djforms.jobpost.views',
    url(r'^data_entered/$',
      view    = 'data_entered',
      name    = 'data_entered',
    ),
    url(r'^maintenance-evs-form/$',
      view    = 'maintenance_form',
      name    = 'maintenance_form',
    ),
)
