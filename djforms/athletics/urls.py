from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.athletics',
    url(
        r'^soccer/camp/success/$',
        TemplateView.as_view(
            template_name="athletics/soccer/camp_registration_done.html"
        ),
        name="soccer_camp_success"
    ),
    url(
        r'^soccer/camp/insurance-card/success/$',
        TemplateView.as_view(
            template_name="athletics/soccer/camp_insurance_card_done.html"
        ),
        name="soccer_camp_insurance_card_success"
    ),
    url(
        r'^soccer/camp/insurance-card/$', 'soccer.views.insurance_card',
        name='soccer_camp_insurance_card'
    ),
    url(
        r'^soccer/camp/$', 'soccer.views.camp_registration',
        name='soccer_camp_registration'
    ),
)
