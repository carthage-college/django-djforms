from django.conf.urls.defaults import *

urlpatterns = patterns('djforms.giving.views',
    url(r'^subscription/success/(?P<campaign>[a-zA-Z0-9_-]+)$', 'subscription_success', name="giving_subscription_success"),
    url(r'^subscription/success/$', 'subscription_success', name="giving_subscription_success"),
    url(r'^subscription/(?P<campaign>[a-zA-Z0-9_-]+)/$', 'subscription', name='giving_subscription'),
    url(r'^subscription/$', 'subscription', name='giving_subscription'),
)
