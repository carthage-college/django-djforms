# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from djforms.admissions.visitdays import views as visitdays
from djforms.admissions.admitted import views as admitted


urlpatterns = [
    path(
        'admitted/success/',
        TemplateView.as_view(template_name='admissions/admitted/success.html'),
        name='admitted_success',
    ),
    path('admitted/', admitted.chance_form, name='chance_form'),
]
