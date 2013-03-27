from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.president.inauguration.forms import RsvpForm
from djtools.utils.mail import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["mfisher@carthage.edu",]
BCC = settings.MANAGERS

def rsvp_form(request):
    if request.method=='POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            subject = "[Inauguration RSVP] %s %s" % (attendee.first_name,attendee.last_name)
            send_mail(request, TO_LIST, subject, attendee.email, "president/inauguration/email.html", attendee, BCC)
            return HttpResponseRedirect('/forms/president/inauguration/success/')
    else:
        form = RsvpForm()
    return render_to_response("president/inauguration/form.html", {"form": form,}, context_instance=RequestContext(request))
