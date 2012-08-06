from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('djforms.adulted.views',
    url(r'^$', redirect_to, {'url': '/adult/', 'permanent': True}),
    url(r'^admissions/success/$', direct_to_template, {'template': 'adulted/admissions_done.html'}, name='adulted_admissions_success'),
    url(r'^admissions/$', 'admissions_form', name='adulted_admissions_form'),
)
