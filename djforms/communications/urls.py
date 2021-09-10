# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.communications.metamorphosis.models import Questionnaire
from djforms.communications.printrequest import views as printrequest
from djforms.communications.metamorphosis import views as metamorphosis


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
    # How has your student changed since their freshman year?
    path(
        'metamorphosis/success/',
        TemplateView.as_view(
            template_name='communications/metamorphosis/done.html',
        ),
        name='metamorphosis_questionnaire_success',
    ),
    path(
        'metamorphosis/<int:quid>/detail/',
        metamorphosis.questionnaire_detail,
        name='metamorphosis_questionnaire_detail',
    ),
    path(
        'metamorphosis/archives/',
        TemplateView.as_view(
            template_name='communications/metamorphosis/archives.html',
        ),
        {'data':Questionnaire.objects.all()},
        name='metamorphosis_questionnaire_archives',
    ),
    path(
        'metamorphosis/<str:who>/',
        metamorphosis.questionnaire_form,
        name='metamorphosis_questionnaire_form',
    ),
]
