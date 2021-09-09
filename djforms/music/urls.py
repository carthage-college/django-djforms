# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm
from djforms.music.ensembles.choral import views as choral


urlpatterns = [
    # choral tryouts
    path(
        'ensembles/choral/tryout/success/',
        TemplateView.as_view(
            template_name='music/ensembles/choral/done.html',
        ),
        name='choral_tryout_success',
    ),
    path(
        'ensembles/choral/tryout/manager/',
        choral.manager,
        name='choral_ensemble_manager',
    ),
    path(
        'ensembles/choral/tryout/',
        choral.candidate,
        name='choral_ensemble_candidate',
    ),
]
