from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from djforms.characterquest import views


urlpatterns = [
    url(
        r'^$', RedirectView.as_view(
            url='/forms/character-quest/application/'
        )
    ),
    url(
        r'^success/$', TemplateView.as_view(
            template_name='characterquest/data_entered.html'
        )
    ),
    url(
        r'^application/$',
        views.application_profile_form,
        name='application_profile_form'
    )
]
