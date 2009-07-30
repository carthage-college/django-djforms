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
    
    #For Alpha's contact form environment
    #(r'^contact/', include('djforms.contact_form.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
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
