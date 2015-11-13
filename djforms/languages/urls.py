from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.languages',
    url(
        r'^study-abroad/$',
        'studyabroad.views.study_abroad'
    ),
    url(
        r'^study-abroad/success/$',
        TemplateView.as_view(
            template_name="languages/studyabroad/data_entered.html"
        ),
        name="study_abroad_success"
    ),
    url(
        r'^tle/success/$',
        TemplateView.as_view(
            template_name="languages/tle/data_entered.html"
        ),
        name="tle_success"
    ),
    url(
        r'^tle/(?P<stype>[\d\w]+)/$',
        'tle.views.application_form'
    ),
    url(
        r'^poetry-festival/',
        include('djforms.languages.poetryfestival.urls')
    ),
)
