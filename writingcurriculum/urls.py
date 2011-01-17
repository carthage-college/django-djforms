from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.writingcurriculum.views',
    url(r'^success/$', direct_to_template, {'template': 'writingcurriculum/data_entered.html'}),
    #url(r'^submission/(?P<req_id>\d+)/$', 'submission_detail', name="submission_detail"),
    #url(r'^submission/(?P<req_id>\d+)/update/$', 'submission_update', name="submission_update"),
    #url(r'^submissions/$', 'submissions', name="submissions"),
    url(r'^$', 'submission_form', name='submission_form'),
)