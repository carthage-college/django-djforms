from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.security.views',
    url(r'^success', direct_to_template, {'template': 'security/data_entered.html'}),
    url(r'^parking-appeal/$', 'parking_ticket_appeal_form', name='parking_ticket_appeal_form'),
)
