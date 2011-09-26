from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    # For room and equipment reserve environment
    url(r'^equipment-reserve/$', 'djforms.lis.equipmentform.views.equipment_reserve'),
    url(r'^print-request/$', 'djforms.lis.printjobs.views.print_request'),
    url(r'^room-reserve/$', 'djforms.lis.roomform.views.room_reserve'),
    url(r'^ill/request/(?P<type>[\d\w]+)/$', 'djforms.lis.ill.views.request_form',name="ill_request_form"),
    url(r'^success/$', direct_to_template, {'template': 'lis/data_entered.html'}),
    # lis ito
    url(r'^ito/profile/success/$', direct_to_template, {'template': 'lis/ito/profile_done.html'}),
    url(r'^ito/profile/archives/$', 'djforms.lis.ito.views.profile_archives', name="profile_archives"),
    url(r'^ito/profile/(?P<id>\d+)/update/$', 'djforms.lis.ito.views.profile_form', name="profile_update"),
    url(r'^ito/profile/(?P<id>\d+)/detail/$', 'djforms.lis.ito.views.profile_detail', name="profile_detail"),
    url(r'^ito/profile/$', 'djforms.lis.ito.views.profile_form', name='profile_form'),
)
