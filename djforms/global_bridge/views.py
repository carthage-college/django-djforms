from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.global_bridge import BCC, TO_LIST
from djforms.global_bridge.forms import RegistrationForm

from djtools.utils.mail import send_mail

def index(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_mail(
                request, TO_LIST,
                "Global Bridge Registration",
                contact.email,
                "global_bridge/registration_email.html",
                order, BCC
            )
            return HttpResponseRedirect(
                reverse('global_bridge_registration_success')
            )
    else:
        form = RegistrationForm()
    return render_to_response(
        'global_bridge/registration_form.html',
        {'form': form,}, context_instance=RequestContext(request)
    )
