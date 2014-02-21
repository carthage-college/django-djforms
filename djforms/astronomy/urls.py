from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.astronomy',
    url(
        r'^institute/night-report/success/$',
        TemplateView.as_view(template_name="astronomy/institute/night_report_done.html")
    ),
    url(
        r'^institute/night-report/$', 'institute.views.night_report', name='night_report'
    ),
    url(
        r'^institute/evaluation/success/$',
        TemplateView.as_view(template_name="astronomy/institute/evaluation_done.html")
    ),
    url(
        r'^institute/evaluation/$', 'institute.views.evaluation', name='evaluation'
    ),
)
