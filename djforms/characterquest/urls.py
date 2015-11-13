from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.characterquest.views',
    url(
        r'^$', RedirectView.as_view(
            url='/forms/character-quest/application/'
        )
    ),
    url(
        r'^success/$', TemplateView.as_view(
            template_name="characterquest/data_entered.html"
        )
    ),
    url(
        r'^application/$',
        'application_profile_form', name='application_profile_form'
    ),
)
