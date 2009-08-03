from django.conf.urls.defaults import *
from djforms.roomform.reserve.views import *
from djforms.equipmentform.reserve.views import *
from djforms.views import *
from djforms.core.views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #For room and equipment reserve environment
    (r'^equipment_reserve/$', equipment_reserve),
    (r'^room-reserve/$', room_reserve),
    (r'^reserve-complete/$', reserve_complete),
    
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'djforms.core.util.admin_list_export'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #for membrete environment
    (r'^contact/', include('djforms.membrete.urls')),
    
    #For edu form environment
    (r'^eduform/data-entered/$', data_entered),
    #catches the slugs
    (r'^eduform/(?P<slug>[-\w]+)/$', add_object),
    
    #for the job post environment
    (r'^job/', include('djforms.jobpost.urls')),
)
