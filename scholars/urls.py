from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.scholars.views',
    url(r'^presentation/success/$', direct_to_template, {'template': 'scholars/presentation/done.html'}),
    url(r'^presentation/(?P<pid>\d+)/detail/$', 'presentation.detail', name="presentation_detail"),
    url(r'^presentation/(?P<pid>\d+)/update/$', 'presentation.form', name="presentation_update"),
    url(r'^presentation/$', 'presentation.form', name="presentation_form"),
    url(r'^archives/(?P<year>\d{4})/(?P<medium>[-\w]+)/$', 'presentation.archives', name="presentation_archives"),
    url(r'^archives/(?P<medium>[-\w]+)/$', 'presentation.archives'),
    url(r'^archives/$', 'presentation.archives'),
)
