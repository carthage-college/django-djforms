# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.alumni.classnotes import views as classnotes


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(template_name='alumni/data_entered.html'),
    ),
    # classnotes
    path(
        'classnotes/carthaginian/',
        classnotes.screenscrape,
        name='classnotes_carthaginian',
    ),
    path(
        'classnotes/success/',
        TemplateView.as_view(template_name='alumni/classnotes/done.html'),
        name='classnotes_success',
    ),
    path(
        'classnotes/archives/<int:year>/',
        classnotes.archives,
        name='classnotes_archives_year',
    ),
    path(
        'classnotes/archives/',
        classnotes.archives,
        name='classnotes_archives',
    ),
    path(
        'classnotes/inmemoriam/',
        classnotes.obits,
        name='classnotes_obits',
    ),
    path(
        'classnotes/',
        classnotes.contact,
        name='classnotes_form',
    ),
]
