from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader

from djforms.alumni.homecoming.forms import AttendeeForm
from djforms.alumni.homecoming.models import Attendee

import datetime

def attendance(request):
    if request.method=='POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            bcc = settings.MANAGERS
            #recipient_list = ["mfisher@carthage.edu",]
            recipient_list = ["larry@carthage.edu",]
            t = loader.get_template('alumni/homecoming/attendance_email.html')
            c = RequestContext(request, {'attendee':attendee,})
            email = EmailMessage(("[Homecoming Attendee] %s %s" % (attendee.first_name,attendee.last_name)), t.render(c), attendee.email, recipient_list, bcc, headers = {'Reply-To': attendee.email,'From': attendee.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/alumni/homecoming/success/')
    else:
        form = AttendeeForm()
    return render_to_response("alumni/homecoming/attendance_form.html", {"form": form,}, context_instance=RequestContext(request))

def attendees(request, year=None):
    if year:
        year = int(year)
    else:
        year = int(datetime.date.today().year)
    attendees = Attendee.objects.filter(created_on__year=year).order_by("-grad_class", "last_name")
    return render_to_response("alumni/homecoming/attendance_archives.html", {"attendees": attendees,"year":year,}, context_instance=RequestContext(request))
