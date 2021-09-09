# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.writingcurriculum import views


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(template_name='writingcurriculum/done.html'),
        name='proposal_success',
    ),
    path(
        'proposal/<int:pid>/update/',
        views.proposal_form,
        name='proposal_update',
    ),
    path(
        'proposal/archives/',
        views.my_proposals,
        name='my_proposals',
    ),
    path('', views.proposal_form, name='proposal_form'),
]
