from django.conf.urls import patterns, url

urlpatterns = patterns('djforms.giving.views',
    url(
        r'^donors/$', 'donors', name='giving_donors'
    ),
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/(?P<campaign>[a-zA-Z0-9_-]+)/success/$',
        'giving_success', name="giving_success_campaign"
    ),
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/success/$',
        'giving_success', name="giving_success_generic"
    ),
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/(?P<campaign>[a-zA-Z0-9_-]+)',
        'giving_form', name='giving_form_campaign'
    ),
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/$',
        'giving_form', name='giving_form_generic'
    ),
)
