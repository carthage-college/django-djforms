from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    # For room and equipment reserve environment
    url(r'^study-abroad/success$', direct_to_template, {'template': 'languages/studyabroad/data_entered.html'}),
    (r'^study-abroad/$', 'djforms.languages.studyabroad.views.study_abroad'),
    (r'^tle/(?P<type>[\d\w]+)/$', 'djforms.languages.tle.views.application_form'),
)
