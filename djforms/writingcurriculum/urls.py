# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.writingcurriculum import views


urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(template_name='writingcurriculum/done.html'),
        name='proposal_success',
    ),
    url(
        r'^proposal/(?P<pid>\d+)/update/$',
        views.proposal_form,
        name='proposal_update',
    ),
    url(
        r'^proposal/archives/$',
        views.my_proposals,
        name='my_proposals',
    ),
    url(
        r'^$',
        views.proposal_form,
        name='proposal_form',
    ),
]
