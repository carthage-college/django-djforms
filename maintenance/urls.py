from django.conf.urls.defaults import *
from djforms.maintenanceform.views import *

urlpatterns = patterns('djforms.jobpost.views',
    url(r'^data_entered/$',
      view    = 'data_entered',
      name    = 'data_entered',
    ),
    url(r'^evs_form/$',
      view    = 'maintenance_evs_form',
      name    = 'maintenance_evs_form',
    ),
)
