from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from djforms.catering.views import CateringEventWizard
from djforms.catering.forms import EventForm1, EventForm2, EventForm3
from djforms.catering.forms import EventForm4, EventForm5
from djforms.catering import views


urlpatterns = [
    url(
        r'^event/archives/$', views.event_archives,
        name='event_archives'
    ),
    url(
        r'^event/(?P<eid>\d+)/detail/$',
        views.event_detail,
        name='catering_event_detail'
    ),
    url(
        r'^event/success/$',
        TemplateView.as_view(template_name='catering/event_done.html'),
        name='catering_event_success'
    ),
    url(
        r'^event/$', login_required(
            CateringEventWizard.as_view(
                [EventForm1, EventForm2, EventForm3, EventForm4, EventForm5]
            )
        )
    )
]
