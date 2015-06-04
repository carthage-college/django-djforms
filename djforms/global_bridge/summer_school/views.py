from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.global_bridge.summer_school import BCC, TO_LIST, REG_FEE
from djforms.global_bridge.summer_school.forms import RegistrationForm

from djtools.utils.mail import send_mail

def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_mail(
                request, TO_LIST,
                "Global bridge Summer School Registration",
                contact.email,
                "global_bridge/summer_school/registration_email.html",
                order, BCC
            )
            return HttpResponseRedirect(
                reverse('global_bridge_summer_school_registration_success')
            )
    else:
        form = RegistrationForm()
    return render_to_response(
        'global_bridge/summer_school/registration_form.html',
        {'form': form,}, context_instance=RequestContext(request)
    )
