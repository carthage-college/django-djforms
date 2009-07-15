# -*- coding: utf-8 -*-

# Copyright © 2009 Gonzalo Delgado
#
# This file is part of membrete.
#
# membrete is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# membrete is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with membrete. If not, see
# <http://www.gnu.org/licenses/>.

from djforms.membrete.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from djforms.membrete.decorators import require_referer_view

#sent = require_referer_view('membrete_contact')(direct_to_template)
urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', 'djforms.membrete.views.contact', name='membrete_contact'),
    #url(r'^(?P<slug>[-\w]+)/sent/', sent, {'template': 'membrete/sent.html'}, name='membrete_sent'),
    url(r'^(?P<slug>[-\w]+)/sent/', direct_to_template,{'template': 'membrete/sent.html'}, name='membrete_sent'),
    url(r'jsi18n$', 'django.views.i18n.javascript_catalog',
                                          {'packages': 'membrete'}, 'jsi18n'),
)
