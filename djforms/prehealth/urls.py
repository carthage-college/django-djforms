# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.prehealth.committee_letter import views


urlpatterns = [
    path(
        'committee-letter/success/',
        TemplateView.as_view(
            template_name='prehealth/committee_letter/done.html',
        ),
        name='prehealth_committee_letter_applicant_success',
    ),
    path(
        'committee-letter/evaluation/success/',
        TemplateView.as_view(
            template_name='prehealth/committee_letter/evaluation/done.html',
        ),
        name='prehealth_committee_letter_evaluation_success',
    ),
    path(
        'committee-letter/<int:aid>/detail/',
        views.applicant_detail,
        name='prehealth_committee_letter_applicant_detail',
    ),
    path(
        'committee-letter/<int:aid>/evaluation/',
        views.evaluation_form,
        name='prehealth_committee_letter_evaluation_form',
    ),
    path(
        'committee-letter/',
        views.applicant_form,
        name='prehealth_committee_letter_applicant_form',
    ),
]
