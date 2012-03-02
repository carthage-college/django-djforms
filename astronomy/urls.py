from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.astronomy',
    url(r'^institute/night-report/success/$', direct_to_template, {'template': 'astronomy/institute/night_report_done.html'}),
    url(r'^institute/night-report/$', 'institute.views.night_report', name='night_report'),
)
