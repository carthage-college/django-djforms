from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    # For room and equipment reserve environment
    (r'^equipment-reserve/$', 'djforms.lis.equipmentform.views.equipment_reserve'),
    (r'^print-request/$', 'djforms.lis.printjobs.views.print_request'),
    (r'^room-reserve/$', 'djforms.lis.roomform.views.room_reserve'),
    (r'^ill/request/(?P<type>[\d\w]+)/$', 'djforms.lis.ill.views.request_form'),
    url(r'^success/$', direct_to_template, {'template': 'lis/data_entered.html'}),
)