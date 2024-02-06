# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.giving import views


urlpatterns = [
    # list of donors displayed
    path('donors/<str:slug>/', views.donors, name='giving_donors_campaign'),
    path('donors/', views.donors, name='giving_donors'),
    # manager views
    path('manager/ajax/', views.manager_ajax, name='manager_ajax'),
    path('manager/cash/', views.manager_cash, name='giving_manager_cash'),
    path(
        'manager/success/',
        TemplateView.as_view(template_name='giving/manager/success.html'),
        name='giving_manager_success',
    ),
    path('manager/photo/', views.photo_caption, name='photo_caption'),
    path(
        'manager/<str:slug>/',
        views.manager,
        name='giving_manager_home_campaign',
    ),
    path('manager/', views.manager, name='giving_manager_home'),
    # ajax calls for campaign, mini-goal, crowd fund challenge, etc.
    path(
        'campaign/<str:slug>/',
        views.promotion_ajax,
        name='promotion_ajax',
    ),
    # displayed after form is submitted
    path(
        '<str:transaction>/<str:campaign>/success/',
        views.giving_success,
        name='giving_success_campaign',
    ),
    path(
        '<str:transaction>/success/',
        views.giving_success,
        name='giving_success_generic',
    ),
    # campaign donation forms
    path(
        '<str:transaction>/<str:campaign>/',
        views.giving_form,
        name='giving_form_campaign',
    ),
    # generic giving
    path(
        '<str:transaction>/',
        views.giving_form,
        name='giving_form_generic',
    ),
]
