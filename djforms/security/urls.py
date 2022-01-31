# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.security import views


urlpatterns = [
    path(
        'parking-appeal/success/',
        TemplateView.as_view(
            template_name='security/parking_ticket_appeal/done.html',
        ),
        name='parking_ticket_appeal_success',
    ),
    path(
        'parking-appeal/',
        views.parking_ticket_appeal,
        name='parking_ticket_appeal',
    ),
    path(
        'anonymous-report/success/',
        TemplateView.as_view(
            template_name='security/anonymous_report/done.html',
        ),
        name='anonymous_report_success',
    ),
    path(
        'anonymous-report/',
        views.anonymous_report,
        name='anonymous_report',
    ),
]
