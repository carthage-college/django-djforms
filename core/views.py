from django.conf import settings
from django.template import RequestContext
from django.template import loader, Context
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage

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

def send_mail(request, recipients, subject, femail, template, data, bcc=None):
        if not bcc:
            bcc = settings.MANAGERS
        t = loader.get_template(template)
        c = RequestContext(request, {'data':data,})
        email = EmailMessage(subject, t.render(c), femail, recipients, bcc, headers = {'Reply-To': femail,'From': femail})
        email.content_subtype = "html"
        email.send(fail_silently=True)

def not_in_group(user):
    if user:
        staff = user.groups.filter(name='Staff').count() == 0
        faculty = user.groups.filter(name='Faculty').count() == 0
        notin = False
        if staff or faculty:
            notin = True
        return group
    return False
