from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^green/pledge/success/$', direct_to_template, {'template': 'sustainability/green/pledge_done.html'}),
    url(r'^green/pledge/archives', 'djforms.sustainability.green.views.pledge_archives', name="pledge_archives"),
    url(r'^green/pledge/$', 'djforms.sustainability.green.views.pledge_form', name="pledge_form"),
)
