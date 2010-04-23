from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.lacrossegolfinvite.views',
    url(r'^success/$', direct_to_template, {'template': 'lacrossegolfinvite/data_entered.html'}),
    url(r'^$', 'lacrosse_golf_invite_form', name='lacrosse_golf_invite_form'),
)
