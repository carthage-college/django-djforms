# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djauth.views import loggedout
from djforms.core.util import admin_list_export

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # home
    path('', RedirectView.as_view(url='https://www.carthage.edu/bridge/')),
    # simple 400 error view
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path('accounts/', RedirectView.as_view(url=reverse_lazy('auth_login'))),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # CSV
    path(
        'admin/<str:app_label>/<str:model_name>/csv/',
        admin_list_export,
        name='admin_list_export',
    ),
    # admin
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls),
    # alumni
    path('alumni/', include('djforms.alumni.urls')),
    # LIS
    path('lis/', include('djforms.lis.urls')),
    # music
    path('music/', include('djforms.music.urls')),
    # polisci
    path('political-science/', include('djforms.polisci.urls')),
    # celebration of scholars
    path('scholars/', include('djforms.scholars.urls')),
    # for the security appeal form environment
    path('security/', include('djforms.security.urls')),
    path('summernote/', include('django_summernote.urls')),
    # writing across curriculum
    path('writingcurriculum/', include('djforms.writingcurriculum.urls')),
    # recaptcha
    path('captcha/', include('captcha.urls')),
]
