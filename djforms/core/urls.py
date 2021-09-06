from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, RedirectView

from djforms.core.util import admin_list_export

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # home
    url(
        r'^$', RedirectView.as_view(url='https://www.carthage.edu/bridge/')
    ),
    # simple 400 error view
    url(
        r'^denied/$',
        TemplateView.as_view(
            template_name='denied.html'
        ), name='access_denied'
    ),
    # auth
    url(
        r'^accounts/login',
        auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',
        auth_views.logout,
        {'next_page': '/forms/accounts/loggedout/'},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout',
        loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$', RedirectView.as_view(url='/forms/')
    ),
    # CSV
    url(
        r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/',
        admin_list_export,
        name='admin_list_export'
    ),
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # admissions
    url(r'^admissions/', include('djforms.admissions.urls')),
    # alumni
    url(r'^alumni/', include('djforms.alumni.urls')),
    # athletics
    url(r'^athletics/', include('djforms.athletics.urls')),
    # communications
    url(r'^communications/', include('djforms.communications.urls')),
    # giving
    url(r'^giving/', include('djforms.giving.urls')),
    # LIS
    url(r'^lis/', include('djforms.lis.urls')),
    # for the modern language form environment
    url(r'^languages/', include('djforms.languages.urls')),
    # music
    url(r'^music/', include('djforms.music.urls')),
    # polisci
    url(r'^political-science/', include('djforms.polisci.urls')),
    # pre-health
    url(r'^pre-health/', include('djforms.prehealth.urls')),
    # for the security appeal form environment
    url(r'^scholars/', include('djforms.scholars.urls')),
    # for the security appeal form environment
    url(r'^security/', include('djforms.security.urls')),
    # writing across curriculum
    url(r'^writingcurriculum/', include('djforms.writingcurriculum.urls'))
]
urlpatterns += url('admin/', include('loginas.urls')),
urlpatterns += url(r'^captcha/', include('captcha.urls')),
