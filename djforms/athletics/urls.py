from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.athletics',
    url(
        r'^soccer/camp/success/$',
        TemplateView.as_view(template_name="athletics/soccer/camp_registration_done.html")
    ),
    url(r'^soccer/camp/$', 'soccer.views.camp_registration', name='soccer_camp_registration'),
)
