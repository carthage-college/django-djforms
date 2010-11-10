from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^success/$', direct_to_template, {'template': 'admissions/data_entered.html'}),
)
