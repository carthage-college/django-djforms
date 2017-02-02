from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('djforms.prehealth',
    url(
        r'^committee-letter/success/$',
        TemplateView.as_view(
            template_name='prehealth/committee_letter/done.html'
        ),
        name='prehealth_committee_letter_applicant_success'
    ),
    url(
        r'^committee-letter/evaluation/success/$',
        TemplateView.as_view(
            template_name='prehealth/committee_letter/evaluation/done.html'
        ),
        name='prehealth_committee_letter_evaluation_success'
    ),
    url(
        r'^committee-letter/(?P<aid>\d+)/detail/$',
        'committee_letter.views.applicant_detail',
        name='prehealth_committee_letter_applicant_detail'
    ),
    url(
        r'^committee-letter/(?P<aid>\d+)/evaluation/$',
        'committee_letter.views.evaluation_form',
        name='prehealth_committee_letter_evaluation_form'
    ),
    url(
        r'^committee-letter/$',
        'committee_letter.views.applicant_form',
        name='prehealth_committee_letter_applicant_form'
    ),
)
