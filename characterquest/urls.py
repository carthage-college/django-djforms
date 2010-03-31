from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('djforms.characterquest.views',
    url(r'^$', redirect_to, {'url': '/forms/character-quest/application/', 'permanent': True}),
    url(r'^data-entered/$', direct_to_template, {'template': 'characterquest/data_entered.html'}),
    url(r'^application/$', 'application_profile_form', name='application_profile_form'),
)
