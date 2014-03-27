from django.conf.urls.defaults import *

urlpatterns = patterns('djforms.giving.views',
    url(r'^(?P<transaction>[a-zA-Z0-9_-]+)/success/(?P<campaign>[a-zA-Z0-9_-]+)', 'giving_success', name="giving_success_campaign"),
    #url(r'^(?P<transaction>[a-zA-Z0-9_-]+)/success/$', 'giving_success', name="giving_success_generic"),
    url(r'^(?P<transaction>[a-zA-Z0-9_-]+)/success', 'giving_success', name="giving_success_generic"),
    url(r'^(?P<transaction>[a-zA-Z0-9_-]+)/(?P<campaign>[a-zA-Z0-9_-]+)', 'giving_form', name='giving_form_campaign'),
    url(r'^(?P<transaction>[a-zA-Z0-9_-]+)/', 'giving_form', name='giving_form_generic'),
)
