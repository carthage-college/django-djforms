from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.languages.studyabroad.views import study_abroad
from djforms.languages.tle import views as tle


urlpatterns = [
    url(
        r'^study-abroad/$', study_abroad
    ),
    url(
        r'^study-abroad/success/$',
        TemplateView.as_view(
            template_name='languages/studyabroad/data_entered.html'
        ),
        name='study_abroad_success'
    ),
    url(
        r'^tle/success/$',
        TemplateView.as_view(
            template_name='languages/tle/data_entered.html'
        ),
        name='tle_success'
    ),
    url(
        r'^tle/(?P<stype>[\d\w]+)/$',
        tle.application_form
    )
]
