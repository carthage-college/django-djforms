# -*- coding: utf-8 -*-

import logging
from django.utils import simplejson
from django.template import RequestContext
from django.utils.encoding import force_unicode
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from djforms.contact.conf import settings
from djforms.contact.models import Message
from djforms.contact.forms import ContactForm
from djforms.contact.decorators import require_referer_view

logger = logging.getLogger('views')


def contact(request,
            slug,
            form_class=ContactForm,
            fail_silently=settings.FAIL_SILENTLY,
            template_name='contact/default.html',
            extra_context={}):
    """
    Valida los datos del formulario de contacto, envía el mensaje por correo
    a los destinatarios y guarda el mensaje en la base de datos.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.send(slug=slug, fail_silently=fail_silently)
            return HttpResponseRedirect(reverse('contact_sent', kwargs={'slug':slug}))
    else:
        form = form_class()
    context = {'form': form}
    user = request.user
    if user.is_active:
        user_can_receive_msg = user.has_perm('contact.can_receive_messages')
        # Si es un usuario que pueda recibir mensajes de contacto, los podrá
        # ver por web. Lo mismo para los usuarios del staff
        if user_can_receive_msg or user.is_staff or user.is_active:
            messages = Message.objects.all()
            context.update({'messages': messages})
    context.update(extra_context)
    return render_to_response(template_name, RequestContext(request, context))
