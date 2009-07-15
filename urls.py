from django.conf.urls.defaults import *
from djforms.roomform.reserve.views import *
from djforms.equipmentform.reserve.views import *
from djforms.views import *
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^equipment_reserve/$', equipment_reserve),
    (r'^room_reserve/$', room_reserve),
    (r'^reserve_complete/$', reserve_complete),
    #(r'^contact/', include('djforms.contact_form.urls')),
    (r'^contact/', include('djforms.membrete.urls')),
    #(r'^admin/', include(admin.site.urls)),
    # Example:
    # (r'^roomreserveform/', include('roomreserveform.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
)
