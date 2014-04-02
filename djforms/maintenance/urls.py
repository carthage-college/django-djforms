from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.maintenance.views',
    url(
        r'^success',
        TemplateView.as_view(template_name="maintenance/data_entered.html"),
        name="maintenance_request_success"
    ),
    url(
        r'^request/(?P<req_id>\d+)/$',
        'maintenance_request_detail',name="maintenance_request_detail"
    ),
    url(
        r'^request/(?P<req_id>\d+)/update/$',
        'maintenance_request_update',name="maintenance_request_update"
    ),
    url(
        r'^requests/$','maintenance_requests',name="maintenance_requests"
    ),
    url(
        r'^$','maintenance_request_form',name='maintenance_request_form'
    ),
)
