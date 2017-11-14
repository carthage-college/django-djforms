from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.writingcurriculum import views


urlpatterns = [
    url(
        r'^success/$', TemplateView.as_view(
            template_name='writingcurriculum/done.html'
        )
    ),
    url(
        r'^proposal/(?P<pid>\d+)/update/$',
        views.proposal_form,
        name='proposal_update'
    ),
    url(
        r'^proposal/archives/$',
        views.my_proposals,
        name='my_proposals'
    ),
    url(
        r'^$',
        views.proposal_form,
        name='proposal_form'
    )
]
