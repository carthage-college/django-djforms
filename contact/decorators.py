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

import re
from inspect import isfunction
from django.http import Http404
from django.core.urlresolvers import resolve, reverse, get_callable


def require_referer_view(referer, slug):
    """
    Returns a decorator which compares the referer of the `viewfunc' view
    against the `referer' argument, which can either be a view, a view name,
    or a url path.
    If the current view referer doesn't match, a Http404 error is raised.
    """
    def decorator(viewfunc):
        def inner(request, *args, **kwargs):
            re1 = '^(?P<proto>http|https)'
            re2 = ':\/{2}'
            re3 = '(?P<server_name>\w+(?:\.\w+)*)'
            re4 = '(?::(?P<server_port>\d+)){0,1}'
            re5 = '(?P<path>(?:\/(?:[-\w~!$+|.,=\(\)]|%[a-f\d]{2})*)+)'
            rg = re.compile(re1+re2+re3+re4+re5)
            request_referer = request.META.get('HTTP_REFERER', '')
            match = rg.match(request_referer)
            if match:
                path = match.groupdict().get('path', '')
                str_match = path == referer or path == reverse(referer, kwargs = {'slug':slug})
                callable_match = get_callable(path) is referer or \
                                 resolve(path)[0] is referer
                if str_match or callable_match:
                    return viewfunc(request, *args, **kwargs)
            raise Http404
        inner.__doc__ = viewfunc.__doc__
        inner.__dict__ = viewfunc.__dict__
        inner.__name__ = viewfunc.__name__
        return inner
    return decorator
