from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY

def loggedout(request, template_name='accounts/logged_out.html'):
    """
    Remove the authenticated user's ID from the request.
    """
    # django auth
    try:
        del request.session[SESSION_KEY]
    except KeyError:
        pass
    try:
        del request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

    return render_to_response(template_name, context_instance=RequestContext(request))
