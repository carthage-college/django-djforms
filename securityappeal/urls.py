from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.securityappeal.views',
    url(r'^request-sent/$', direct_to_template, {'template': 'securityappeal/request-sent.html'}),
    url(r'^$', 'security_appeal_form', name='security_appeal_form'),
)
