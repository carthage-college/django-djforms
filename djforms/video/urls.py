from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/videos/', 'permanent': True}),
    url(r'^success/$', direct_to_template, {'template': 'video/contest_done.html'}),
    url(r'^entry/$', 'djforms.video.views.contest_form', name='contest_form'),
    url(r'^entry/(?P<tag>.*)/archives', 'djforms.video.views.contest_archives', name='contest_archives'),
)
