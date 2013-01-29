from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('djforms.lis',
    # For room and equipment reserve environment
    url(r'^secure/reference/articles', direct_to_template, {'template': 'lis/secure/reference/articles.html'}),
    url(r'^equipment-reserve/$', 'equipmentform.views.equipment_reserve'),
    url(r'^print-request/$', 'printjobs.views.print_request'),
    url(r'^room-reserve/$', 'roomform.views.room_reserve'),
    url(r'^ill/request/(?P<type>[\d\w]+)/$', 'ill.views.request_form',name="ill_request_form"),
    url(r'^success', direct_to_template, {'template': 'lis/data_entered.html'}),
    # lis ito
    url(r'^ito/profile/success', direct_to_template, {'template': 'lis/ito/profile_done.html'}),
    url(r'^ito/profile/archives', 'ito.views.profile_archives', name="profile_archives"),
    url(r'^ito/profile/(?P<pid>\d+)/update/$', 'ito.views.profile_form', name="profile_update"),
    url(r'^ito/profile/(?P<pid>\d+)/detail/$', 'ito.views.profile_detail', name="profile_detail"),
    url(r'^ito/profile/$', 'ito.views.profile_form', name='profile_form'),
    # conference registration
    url(r'^conferences/looking-glass/success/$', direct_to_template, {'template': 'lis/conferences/looking_glass/done.html'}, name="looking_glass_registration_success"),
    url(r'^conferences/looking-glass/$', 'conferences.looking_glass.views.registration_form', name='looking_glass_registration_form'),
)
