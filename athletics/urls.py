from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.athletics',
    url(r'^soccer/camp/success/$', direct_to_template, {'template': 'athletics/soccer/camp_registration_done.html'}),
    url(r'^soccer/camp/registration/$', 'soccer.views.camp_registration', name='camp_registration'),
)
