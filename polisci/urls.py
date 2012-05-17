from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('djforms.polisci',
    url(r'^$', redirect_to, {'url': '/political-science/', 'permanent': True}),
    url(r'^model-united-nations/success/$', direct_to_template, {'template': 'polisci/mun/data_entered.html'}),
    url(r'^model-united-nations/registration/$', 'mun.views.registration_form', name='mun_registration_form'),
)
