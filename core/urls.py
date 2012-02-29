from django.contrib import admin
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template, redirect_to
from djforms.core.views import data_entered
from djforms.core.auth.views import loggedout

admin.autodiscover()

handler404 = 'djforms.core.views.four_oh_four_error'
handler500 = 'djforms.core.views.server_error'

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
    (r'^admin/', admin.site.urls),
    # admin/docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admissions
    (r'^admissions/', include('djforms.admissions.urls')),
    # alumni
    (r'^alumni/', include('djforms.alumni.urls')),
    # athletics
    (r'^athletics/', include('djforms.athletics.urls')),
    # biology
    (r'^biology/', include('djforms.biology.urls')),
    # CharacterQuest
    (r'^character-quest/', include('djforms.characterquest.urls')),
    # LIS
    (r'^lis/', include('djforms.lis.urls')),
    # for the job post environment
    (r'^job/', include('djforms.jobpost.urls')),
    # for the modern language form environment
    (r'^languages/', include('djforms.languages.urls')),
    # maintenance/evs
    (r'^maintenance/', include('djforms.maintenance.urls')),
    # polisci
    (r'^political-science/', include('djforms.polisci.urls')),
    # president
    (r'^president/', include('djforms.president.urls')),
    # generic request complete
    (r'^success/$', 'djforms.core.views.data_entered'),
    # for the security appeal form environment
    (r'^security/', include('djforms.security.urls')),
    # sustainability
    (r'^sustainability/', include('djforms.sustainability.urls')),
    # video
    (r'^video/', include('djforms.video.urls')),
    # writing across curriculum
    (r'^writingcurriculum/', include('djforms.writingcurriculum.urls')),
)
