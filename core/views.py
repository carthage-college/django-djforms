from django.conf import settings
from django.template import RequestContext
from django.template import loader, Context
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response

def data_entered(request):
    return render_to_response('data_entered.html')

def server_error(request, template_name='500.html'):
    """
    500 error handler.    Templates: `500.html`
    Context:
        media_url
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(Context({
        'media_url': settings.MEDIA_URL,'layout':[0,1],
    })))

def four_oh_four_error(request, template_name='404.html'):
    """
    404 error handler.

    Templates: `404.html`
    Context:
        media_url
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name)
    return HttpResponseNotFound(t.render(Context({
        'media_url': settings.MEDIA_URL,'layout':[0,1],
    })))

