from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.astronomy',
    url(
        r'^institute/night-report/success/$',
        TemplateView.as_view(
            template_name="astronomy/institute/night_report_done.html"
        ),
        name="cia_night_report_success"
    ),
    url(
        r'^institute/night-report/$',
        'institute.views.night_report',
        name='cia_night_report'
    ),
    url(
        r'^institute/evaluation/success/$',
        TemplateView.as_view(
            template_name="astronomy/institute/evaluation_done.html"
        ),
        name="cia_evaluation_success"
    ),
    url(
        r'^institute/evaluation/$',
        'institute.views.evaluation',
        name='cia_evaluation'
    ),
)
