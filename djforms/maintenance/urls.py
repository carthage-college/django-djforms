from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.maintenance.views',
    url(r'^success', direct_to_template, {'template': 'maintenance/data_entered.html'}),
    url(r'^request/(?P<req_id>\d+)/$', 'maintenance_request_detail', name="maintenance_request_detail"),
    url(r'^request/(?P<req_id>\d+)/update/$', 'maintenance_request_update', name="maintenance_request_update"),
    url(r'^requests/$', 'maintenance_requests', name="maintenance_requests"),
    url(r'^$', 'maintenance_request_form', name='maintenance_request_form'),
)
