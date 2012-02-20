from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.athletics',
    url(r'^soccer/camp/success/$', direct_to_template, {'template': 'athletics/soccer/camp_registration_done.html'}),
    url(r'^soccer/camp/registration/$', 'soccer.views.camp_registration', name='camp_registration'),
    #url(r'^genomics/phage-hunters/archives/$', 'genomics.views.phage_hunter_archives', name="phage_hunter_archives"),
    #url(r'^genomics/phage-hunters/(?P<pid>\d+)/detail/$', 'genomics.views.phage_hunter_detail', name="phage_hunter_detail"),
)
