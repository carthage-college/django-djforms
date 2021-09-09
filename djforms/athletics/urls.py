# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.athletics.soccer import views


urlpatterns = [
    path(
        'soccer/camp/success/',
        TemplateView.as_view(
            template_name='athletics/soccer/camp_registration_done.html',
        ),
        name='soccer_camp_success',
    ),
    path(
        'soccer/camp/insurance-card/success/',
        TemplateView.as_view(
            template_name='athletics/soccer/camp_insurance_card_done.html',
        ),
        name='soccer_camp_insurance_card_success',
    ),
    path(
        'soccer/camp/balance/success/',
        TemplateView.as_view(
            template_name='athletics/soccer/camp_balance_done.html',
        ),
        name='soccer_camp_balance_success',
    ),
    path(
        'soccer/camp/insurance-card/',
        views.insurance_card,
        name='soccer_camp_insurance_card',
    ),
    path('soccer/camp/balance/', views.camp_balance, name='soccer_camp_balance'),
    path('soccer/camp/', views.camp_registration, name='soccer_camp_registration'),
]
