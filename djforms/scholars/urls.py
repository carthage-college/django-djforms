# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from djforms.scholars.views import presentation
from djforms.scholars.views import imprimir


urlpatterns = [
    # print
    path('presentation/print/', imprimir.alpha, name='presentation_print'),
    path(
        'presentation/alpha/', imprimir.alpha,
        {'template':'scholars/print/alpha.html'},
        name='presentation_print_alpha',
    ),
    # archives
    path(
        'archives/<str:ptype>/<str:medium>/<str:year>/',
        presentation.archives,
        name='presentation_archives',
    ),
    path(
        'archives/<str:ptype>/<str:medium>/',
        presentation.archives,
        name='presentation_archives_home',
    ),
    # presentation crud
    path(
        'presentation/success/',
        TemplateView.as_view(template_name='scholars/presentation/done.html'),
        name='presentation_form_done',
    ),
    path(
        'presentation/manager/',
        presentation.manager,
        name='presentation_manager',
    ),
    path(
        'presentation/action/',
        presentation.action,
        name='presentation_action',
    ),
    path(
        'presentation/<int:pid>/update/',
        presentation.form,
        name='presentation_update',
    ),
    path(
        'presentation/<int:pid>/detail/',
        presentation.detail,
        name='presentation_detail',
    ),
    path('presentation/', presentation.home, name='presentation_home'),
    path(
        'presentation/form/',
        presentation.form,
        name='presentation_form',
    ),
    # send email to all presentation leaders
    # 10 Apr 2014: currently not completed but needed for 2015
    #path(
    #    r'^presenters/email/leaders/$',
    #    presentation.email_leaders, name="email_leaders"
    #),
    # send email to a presentation's leader and sponsor
    path(
        'presenters/email/success/',
        TemplateView.as_view(
            template_name='scholars/presenters/email_done.html'
        ),
        name='email_presenters_done',
    ),
    path(
        'presenters/email/all/',
        presentation.email_all_presenters,
        name='email_all_presenters',
    ),
    path(
        'presenters/email/<int:pid>/<str:action>/',
        presentation.email_presenters,
        name='email_presenters_form',
    ),
]
