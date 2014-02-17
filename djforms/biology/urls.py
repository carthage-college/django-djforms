from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.biology',
    url(r'^genomics/phage-hunters/success/$', direct_to_template, {'template': 'biology/genomics/phage_hunter_done.html'}),
    url(r'^genomics/phage-hunters/archives/$', 'genomics.views.phage_hunter_archives', name="phage_hunter_archives"),
    url(r'^genomics/phage-hunters/application/$', 'genomics.views.phage_hunter_form', name='phage_hunter_form'),
    url(r'^genomics/phage-hunters/(?P<pid>\d+)/detail/$', 'genomics.views.phage_hunter_detail', name="phage_hunter_detail"),
)
