from django.contrib import admin
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
from djforms.roomform.reserve.views import *
from djforms.equipmentform.reserve.views import *
from djforms.views import *
from djforms.core.views import *
from djforms.auth.views import loggedout

#import authority

admin.autodiscover()
#authority.autodiscover()

handler404 = 'djforms.core.views.four_oh_four_error'
handler500 = 'djforms.core.views.server_error'

urlpatterns = patterns('',
    # home
    (r'^$', direct_to_template, {'template': 'forms_home.html'}),
    # For room and equipment reserve environment
    (r'^equipment_reserve/$', equipment_reserve),
    (r'^room-reserve/$', room_reserve),
    (r'^reserve-complete/$', reserve_complete),
    # django authoriity
    #(r'^authority/', include('authority.urls')),
    # CSV
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'djforms.core.util.admin_list_export'),
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # for contact forms environment
    (r'^contact/', include('djforms.contact.urls')),
    # for the maintenance/evs form environment
    (r'^maintenance/', include('djforms.maintenance.urls')),
    # for the alumni forms
    (r'^alumni/', include('djforms.alumni.urls')),
    # CharacterQuest
    (r'^character-quest/', include('djforms.characterquest.urls')),
    # For edu form environment
    (r'^eduform/data-entered/$', data_entered),
    # catches the slugs
    (r'^eduform/(?P<slug>[-\w]+)/$', add_object),
    # for the job post environment
    (r'^job/', include('djforms.jobpost.urls')),
    # auth
    url(r'^accounts/login/$',auth_views.login,{'template_name': 'accounts/login.html'},name='auth_login'),
    url(r'^accounts/logout/$',auth_views.logout,{'next_page': '/forms/accounts/loggedout/'}),
    url(r'^accounts/loggedout',loggedout,{'template_name': 'accounts/logged_out.html'}),
)
