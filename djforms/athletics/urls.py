from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.athletics.soccer import views


urlpatterns = [
    url(
        r'^soccer/camp/success/$',
        TemplateView.as_view(
            template_name='athletics/soccer/camp_registration_done.html'
        ),
        name='soccer_camp_success'
    ),
    url(
        r'^soccer/camp/insurance-card/success/$',
        TemplateView.as_view(
            template_name='athletics/soccer/camp_insurance_card_done.html'
        ),
        name='soccer_camp_insurance_card_success'
    ),
    url(
        r'^soccer/camp/insurance-card/$', views.insurance_card,
        name='soccer_camp_insurance_card'
    ),
    url(
        r'^soccer/camp/$', views.camp_registration,
        name='soccer_camp_registration'
    )
]
