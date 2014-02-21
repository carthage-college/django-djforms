from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from djforms.catering.views import CateringEventWizard
from djforms.catering.forms import EventForm1, EventForm2, EventForm3, EventForm4, EventForm5

urlpatterns = patterns('djforms.catering.views',
    url(r'^event/archives/$', 'event_archives', name="event_archives"),
    url(r'^event/(?P<eid>\d+)/detail/$', 'event_detail', name="catering_event_detail"),
    url(
        r'^event/success/$', TemplateView.as_view(template_name="catering/event_done.html")
    ),
    url(
        r'^event/$', login_required(
            CateringEventWizard.as_view(
                [EventForm1, EventForm2, EventForm3, EventForm4, EventForm5]
            )
        )
    ),
)
