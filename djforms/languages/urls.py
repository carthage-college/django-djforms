# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.languages.studyabroad.views import study_abroad
from djforms.languages.tle import views as tle


urlpatterns = [
    path('study-abroad/', study_abroad),
    path(
        'study-abroad/success/',
        TemplateView.as_view(
            template_name='languages/studyabroad/data_entered.html',
        ),
        name='study_abroad_success',
    ),
    path(
        'tle/success/',
        TemplateView.as_view(
            template_name='languages/tle/data_entered.html',
        ),
        name='tle_success',
    ),
    path('tle/<str:stype>/', tle.application_form),
]
