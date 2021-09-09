# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.admissions.visitdays import views as visitdays
from djforms.admissions.admitted import views as admitted


urlpatterns = [
    path(
        'visit/success/',
        TemplateView.as_view(template_name='admissions/visitday/success.html'),
        name='visitday_success',
    ),
    path(
        'visit/',
        TemplateView.as_view(template_name='admissions/visitday/home.html'),
        name='visitday_home',
    ),
    path(
        'visit/<str:event_type>/',
        visitdays.visit_day_form,
        name='visitday_form',
    ),
    path(
        'admitted/success/',
        TemplateView.as_view(template_name='admissions/admitted/success.html'),
        name='admitted_success',
    ),
    path('admitted/', admitted.chance_of_form, name='chance_of_form'),
]
