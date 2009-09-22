# -*- coding: utf-8 -*-
from djforms.membrete.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from djforms.membrete.decorators import require_referer_view

#sent = require_referer_view('membrete_contact')(direct_to_template)
urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', 'djforms.membrete.views.contact', name='membrete_contact'),
    #url(r'^(?P<slug>[-\w]+)/sent/', sent, {'template': 'membrete/sent.html'}, name='membrete_sent'),
    url(r'^(?P<slug>[-\w]+)/sent/', direct_to_template,{'template': 'membrete/sent.html'}, name='membrete_sent'),
    url(r'jsi18n$', 'django.views.i18n.javascript_catalog', {'packages': 'membrete'}, 'jsi18n'),
)
