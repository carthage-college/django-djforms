from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(
        r'^study-abroad/$', 'djforms.languages.studyabroad.views.study_abroad'
    ),
    url(
        r'^study-abroad/success$',
        TemplateView.as_view(template_name="languages/studyabroad/data_entered.html")
    ),
    url(
        r'^tle/(?P<type>[\d\w]+)/$', 'djforms.languages.tle.views.application_form'
    ),
    url(
        r'^tle/success$',
        TemplateView.as_view(template_name="languages/tle/data_entered.html")
    ),
    url(r'^poetry-festival/', include('djforms.languages.poetryfestival.urls')),
)
