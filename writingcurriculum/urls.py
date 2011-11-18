from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.writingcurriculum.views',
    url(r'^success/$', direct_to_template, {'template': 'writingcurriculum/data_entered.html'}),
    #url(r'^proposal/(?P<pid>\d+)/$', 'proposal_detail', name="proposal_detail"),
    url(r'^proposal/(?P<pid>\d+)/update/$', 'proposal_form', name="proposal_update"),
    url(r'^proposal/archives/$', 'my_proposals', name="my_proposals"),
    url(r'^$', 'proposal_form', name='proposal_form'),
)
