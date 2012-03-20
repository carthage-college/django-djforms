from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.dining.views',
    #url(r'^event/archives/$', 'event_archives', name="event_archives"),
    url(r'^event/(?P<pid>\d+)/detail/$', 'request_detail', name="dining_event_request_detail"),
    url(r'^event/success/$', direct_to_template, {'template': 'dining/event_done.html'}),
    url(r'^event/$', 'request_form', name='dining_event_request_form'),
)
