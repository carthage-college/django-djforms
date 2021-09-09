# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.security import views


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(
            template_name='security/parking_ticket_appeal/done.html',
        ),
        name='parking_ticket_appeal_success',
    ),
    path(
        'parking-appeal/',
        views.parking_ticket_appeal_form,
        name='parking_ticket_appeal_form',
    ),
]
