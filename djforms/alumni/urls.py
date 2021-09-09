# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.alumni.classnotes import views as classnotes
from djforms.alumni.distinguished import views as distinguished
from djforms.alumni.memory import views as memory


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
    # distinguised alumni nomination
    path(
        'distinguished/nomination/success/',
        TemplateView.as_view(template_name='alumni/data_entered.html'),
        name='distinguished_nomination_success',
    ),
    path(
        'distinguished/nomination/',
        distinguished.nomination_form,
        name='distinguished_nomination_form',
    ),
    # fond memories
    path(
        'memory/success/',
        TemplateView.as_view(template_name='alumni/memory/done.html'),
        name='memory_questionnaire_success',
    ),
    path(
        'memory/archives/',
        memory.questionnaire_archives,
        name='memory_questionnaire_archives',
    ),
    path(
        'memory/<int:quid>/detail/',
        memory.questionnaire_detail,
        name='memory_questionnaire_detail',
    ),
    path(
        'memory/<str:campaign>/',
        memory.questionnaire_form,
        name='memory_questionnaire_promo_form',
    ),
    path(
        'memory/',
        memory.questionnaire_form,
        name='memory_questionnaire_form',
    ),
]
