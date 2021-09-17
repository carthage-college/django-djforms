# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.communications.printrequest import views as printrequest


urlpatterns = [
    # print request form
    path(
        'print-request/success/',
        TemplateView.as_view(template_name='communications/printrequest/done.html'),
        name='print_request_success',
    ),
    path(
        'print-request/',
        printrequest.print_request,
        name='print_request',
    ),
]
