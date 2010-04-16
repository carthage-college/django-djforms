from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.lacrossegolfinvite.views',
    url(r'^request-sent/$', direct_to_template, {'template': 'lacrossegolfinvite/request-sent.html'}),
    url(r'^$', 'lacrosse_golf_invite_form', name='lacrosse_golf_invite_form'),
)
