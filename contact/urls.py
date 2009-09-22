# -*- coding: utf-8 -*-
from djforms.contact.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from djforms.contact.decorators import require_referer_view

#sent = require_referer_view('contact')(direct_to_template)
urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', 'djforms.contact.views.contact', name='contact'),
    #url(r'^(?P<slug>[-\w]+)/sent/', sent, {'template': 'contact/sent.html'}, name='contact_sent'),
    url(r'^(?P<slug>[-\w]+)/sent/', direct_to_template,{'template': 'contact/sent.html'}, name='contact_sent'),
    url(r'jsi18n$', 'django.views.i18n.javascript_catalog', {'packages': 'contact'}, 'jsi18n'),
)
