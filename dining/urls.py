from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from djforms.dining.views import CateringEventWizard
from djforms.dining.forms import EventForm1, EventForm2, EventForm3, EventForm4, EventForm5

urlpatterns = patterns('djforms.dining.views',
    url(r'^event/archives/$', 'event_archives', name="event_archives"),
    url(r'^event/(?P<eid>\d+)/detail/$', 'event_detail', name="dining_event_detail"),
    url(r'^event/success/$', direct_to_template, {'template': 'dining/event_done.html'}),
    url(r'^event/$', login_required( CateringEventWizard.as_view([EventForm1, EventForm2, EventForm3, EventForm4, EventForm5]) )),
)
