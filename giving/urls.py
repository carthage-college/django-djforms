from django.conf.urls.defaults import *

urlpatterns = patterns('djforms.giving.views',
    url(r'^pledge/success/(?P<campaign>[a-zA-Z0-9_-]+)$', 'pledge_success', name="giving_pledge_success"),
    url(r'^pledge/success/$', 'pledge_success', name="giving_pledge_success"),
    url(r'^pledge/(?P<campaign>[a-zA-Z0-9_-]+)/$', 'pledge', name='giving_pledge'),
    url(r'^pledge/$', 'pledge', name='giving_pledge'),
)
