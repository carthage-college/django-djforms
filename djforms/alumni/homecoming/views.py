from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.alumni.homecoming.forms import AttendeeForm
from djforms.alumni.homecoming.models import Attendee
from djtools.utils.mail import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["alumnioffice@carthage.edu",]
BCC = settings.MANAGERS

def attendance(request):
    if request.method=='POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if attendee.email:
                email = attendee.email
            subject = "[Homecoming Attendee] %s %s" % (attendee.first_name,attendee.last_name)
            send_mail(request, TO_LIST, subject, email, "alumni/homecoming/attendance_email.html", attendee, BCC)
            return HttpResponseRedirect('/forms/alumni/homecoming/success/')
    else:
        form = AttendeeForm()
    return render_to_response("alumni/homecoming/attendance_form.html", {"form": form,}, context_instance=RequestContext(request))

def attendees(request, year=None):
    if year:
        year = int(year)
    else:
        year = int(datetime.date.today().year)
    attendees = Attendee.objects.filter(created_at__year=year).order_by("-grad_class", "last_name")
    return render_to_response("alumni/homecoming/attendance_archives.html", {"attendees": attendees,"year":year,}, context_instance=RequestContext(request))
