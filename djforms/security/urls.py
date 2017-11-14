from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.security import views


urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='security/parking_ticket_appeal/done.html'
        ),
        name='parking_ticket_appeal_success'
    ),
    url(
        r'^parking-appeal/$',
        views.parking_ticket_appeal_form,
        name='parking_ticket_appeal_form'
    )
]
