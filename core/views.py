from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext
from django.template import loader, Context
from django.http import Http404, HttpResponseRedirect, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404

from djforms.core.models import GenericContactForm
from djforms.forms import *
from types import *

def data_entered(request):
    return render_to_response('eduform/data_entered.html')

def add_object(request, slug):
    gform = get_object_or_404(GenericContactForm,slug=slug)
    form = None
    if request.method == 'POST':
        form = eval(gform.form_class)(request.POST)
        if form.is_valid():
            data = form.save()
            t = loader.get_template('eduform/email.txt')
            c = Context({'data':data,})
            recipient_list = []
            for recipient in gform.recipients.all():
                recipient_list.append(recipient.email)
            send_mail(gform.name, t.render(c), form.cleaned_data.get('email'), recipient_list, fail_silently=False)
            return HttpResponseRedirect ('/eduform/data-entered')
    else:
        form = eval(gform.form_class)()
    return render_to_response("eduform/add_form.html", {'form':form,'gform':gform}, context_instance=RequestContext(request))

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

