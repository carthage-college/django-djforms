from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('djforms.poetryfestival.views',
    url(r'^$', 'signup_form', name='signup_form'),
    url(r'^data-entered/$', direct_to_template, {'template': 'poetryfestival/data_entered.html'}),
)
