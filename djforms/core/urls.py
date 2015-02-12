from django.contrib import admin
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, RedirectView

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    # home
    (r'^$', TemplateView.as_view(template_name="forms_home.html")),
    # academics
    #(r'^academics/', include('djforms.academics.urls')),
    # auth
    url(
        r'^accounts/login',
        auth_views.login,{'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',
        auth_views.logout,{'next_page': '/forms/accounts/loggedout/'},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout',
        loggedout,{'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$', RedirectView.as_view(url='/forms/')
    ),
    # CSV
    url(
        r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/',
        'djforms.core.util.admin_list_export'
    ),
    # admin
    (r'^admin/', include(admin.site.urls) ),
    # override user creation
    #(r'^admin/auth/user/add/', 'djauth.views.user_add'),
    # admin/docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admissions
    (r'^admissions/', include('djforms.admissions.urls')),
    # alumni
    (r'^alumni/', include('djforms.alumni.urls')),
    # astronomy
    (r'^astronomy/', include('djforms.astronomy.urls')),
    # athletics
    (r'^athletics/', include('djforms.athletics.urls')),
    # biology
    (r'^biology/', include('djforms.biology.urls')),
    # captcha
    (r'^captcha/', include('captcha.urls')),
    # catering
    (r'^catering/', include('djforms.catering.urls')),
    # CharacterQuest
    (r'^character-quest/', include('djforms.characterquest.urls')),
    # communications
    (r'^communications/', include('djforms.communications.urls')),
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
    # office of the president
    (r'^president/', include('djforms.president.urls')),
    # for the security appeal form environment
    (r'^scholars/', include('djforms.scholars.urls')),
    # for the security appeal form environment
    (r'^security/', include('djforms.security.urls')),
    # sustainability
    (r'^sustainability/', include('djforms.sustainability.urls')),
    # writing across curriculum
    (r'^writingcurriculum/', include('djforms.writingcurriculum.urls')),
)
