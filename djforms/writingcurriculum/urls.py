from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.writingcurriculum.views',
    url(
        r'^success/$', TemplateView.as_view(template_name="writingcurriculum/done.html")
    ),
    url(
        r'^proposal/(?P<pid>\d+)/update/$', 'proposal_form', name="proposal_update"
    ),
    url(
        r'^proposal/archives/$', 'my_proposals', name="my_proposals"
    ),
    url(r'^$', 'proposal_form', name='proposal_form'),
)
