# -*- coding: utf-8 -*-

from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from djforms.spacegrant.conference import views as registration


urlpatterns = [
    path(
        'conference/registration/success/',
        TemplateView.as_view(template_name='spacegrant/conference/done.html'),
        name='spacegrant_registration_success'
    ),
    path(
        'conference/registration/',
        registration.form,
        name='spacegrant_registration'
    ),
    path('', RedirectView.as_view(url=reverse_lazy('spacegrant_registration'))),
]
