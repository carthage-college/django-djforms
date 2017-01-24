from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('djforms.prehealth',
    url(
        r'^committee-letter/success/$',
        TemplateView.as_view(
            template_name="committee_letter/done.html"
        ),
        name="prehealth_committee_letter_success"
    ),
    #url(
    #    r'^committee-letter/(?P<cid>\d+)/detail/$',
    #    'applicant_detail',name="prehealth_committee_letter_applicant_detail"
    #),
    url(
        r'^committee-letter/$', 'committee_letter.views.applicant_form',
        name="prehealth_committee_letter_applicant_form"
    ),
)
