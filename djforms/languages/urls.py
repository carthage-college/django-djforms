from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^study-abroad/$', 'djforms.languages.studyabroad.views.study_abroad'),
    url(r'^study-abroad/success$', direct_to_template, {'template': 'languages/studyabroad/data_entered.html'}),
    url(r'^tle/(?P<type>[\d\w]+)/$', 'djforms.languages.tle.views.application_form'),
    url(r'^tle/success$', direct_to_template, {'template': 'languages/tle/data_entered.html'}),
    # poetry festival sign up form
    url(r'^poetry-festival/', include('djforms.languages.poetryfestival.urls')),
)
