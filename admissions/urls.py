from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/admissions/visit/', 'permanent': True}),
    url(r'^success/$', direct_to_template, {'template': 'admissions/data_entered.html'}),
    url(r'^visit/(?P<event_type>[a-zA-Z0-9_-]+)/$', 'djforms.admissions.visitdays.views.VisitDayForm', name='visit_day_form'),
)
