from django.contrib import admin
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template, redirect_to

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    # home
    (r'^$', direct_to_template, {'template': 'forms_home.html'}),
    # academics
    (r'^academics/', include('djforms.academics.urls')),
    # auth
    url(r'^accounts/login',auth_views.login,{'template_name': 'accounts/login.html'},name='auth_login'),
    url(r'^accounts/logout/$',auth_views.logout,{'next_page': '/forms/accounts/loggedout/'}),
    url(r'^accounts/loggedout',loggedout,{'template_name': 'accounts/logged_out.html'}),
    url(r'^accounts/$', redirect_to, {'url': '/forms/', 'permanent': True}),
    # CSV
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'djforms.core.util.admin_list_export'),
    # admin
    (r'^admin/', include(admin.site.urls) ),
    # admin/docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admissions
    (r'^admissions/', include('djforms.admissions.urls')),
    # adult education
    (r'^adult/', include('djforms.adulted.urls')),
    # alumni
    (r'^alumni/', include('djforms.alumni.urls')),
    # astronomy
    (r'^astronomy/', include('djforms.astronomy.urls')),
    # athletics
    (r'^athletics/', include('djforms.athletics.urls')),
    # biology
    (r'^biology/', include('djforms.biology.urls')),
    # catering
    (r'^catering/', include('djforms.catering.urls')),
    # CharacterQuest
    (r'^character-quest/', include('djforms.characterquest.urls')),
    # giving
    (r'^giving/', include('djforms.giving.urls')),
    # LIS
    (r'^lis/', include('djforms.lis.urls')),
    # for the job post environment
    (r'^job/', include('djforms.jobpost.urls')),
    # for the modern language form environment
    (r'^languages/', include('djforms.languages.urls')),
    # maintenance/evs
    (r'^maintenance/', include('djforms.maintenance.urls')),
    # music
    (r'^music/', include('djforms.music.urls')),
    # polisci
    (r'^political-science/', include('djforms.polisci.urls')),
    # for the security appeal form environment
    (r'^security/', include('djforms.security.urls')),
    # for the security appeal form environment
    (r'^scholars/', include('djforms.scholars.urls')),
    # sustainability
    (r'^sustainability/', include('djforms.sustainability.urls')),
    # video
    (r'^video/', include('djforms.video.urls')),
    # writing across curriculum
    (r'^writingcurriculum/', include('djforms.writingcurriculum.urls')),
)
