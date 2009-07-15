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

from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', True)
MAIL_ADMINS = getattr(settings, 'MEMBRETE_MAIL_ADMINS', False)
MAIL_MANAGERS = getattr(settings, 'MEMBRETE_MAIL_MANAGERS', True)
USE_FORM_EMAIL = getattr(settings, 'MEMBRETE_USE_FORM_EMAIL', False)
FROM_EMAIL = getattr(settings,
                     'MEMBRETE_FROM_EMAIL',
                     'webmaster@carthage.edu')
NOTIFY_SENT = getattr(settings, 'MEMBRETE_NOTIFY_SENT', True)
FAIL_SILENTLY = getattr(settings, 'MEMBRETE_FAIL_SILENTLY', True)
DEFAULT_TEMPLATE = 'membrete/message.txt'
