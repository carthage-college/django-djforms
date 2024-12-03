# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.lis.copyprint import views as copyprint
from djforms.lis.printjobs import views as printjobs
from djforms.lis.pages import views as pages


urlpatterns = [
    # copy/print card request
    path('copy-print/', copyprint.index),
    # pages
    path('downloads/', pages.downloads),
    # print requests
    path('print-request/', printjobs.index),
    # print requests success
    path(
        'print-request/success/',
        TemplateView.as_view(template_name='lis/printjobs/data_entered.html'),
        name='print_request_success',
    ),
    # generic success view
    path(
        'success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name='lis_success',
    ),
]
