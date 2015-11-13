from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.security.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name="security/parking_ticket_appeal/done.html"
        ),
        name="parking_ticket_appeal_success"
    ),
    url(
        r'^parking-appeal/$',
        'parking_ticket_appeal_form',
        name='parking_ticket_appeal_form'
    ),
)
