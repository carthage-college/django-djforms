from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    # For room and equipment reserve environment
    (r'^study-abroad/$', 'djforms.languages.studyabroad.views.study_abroad'),
    (r'^tle/application/(?P<type>[\d\w]+)/$', 'djforms.languages.tle.views.application_form'),
    url(r'^success/$', direct_to_template, {'template': 'lis/data_entered.html'}),
)
