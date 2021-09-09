# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from djforms.polisci.mun import views as mun


urlpatterns = [
    path(
        'model-united-nations/success/',
        TemplateView.as_view(
            template_name='polisci/mun/done.html',
        ),
        name='model_united_nations_success',
    ),
    path(
        'model-united-nations/registration/',
        mun.registration,
        name='model_united_nations_registration',
    ),
    # had to revert to old reg form
    #path(
    #    'model-united-nations/success/',
    #    TemplateView.as_view(
    #        template_name='polisci/model_united_nations/done.html',
    #    ),
    #    name='model_united_nations_success',
    #),
    #path(
    #    'model-united-nations/registration/$',
    #    'model_united_nations.views.registration',
    #    name='model_united_nations_registration'
    #),
    path('', RedirectView.as_view(url='/political-science/')),
]
