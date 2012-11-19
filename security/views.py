from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import EmailMessage

from djforms.security.forms import ParkingTicketAppealForm
from djtools.utils.mail import send_mail

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["parking@carthage.edu",]
BCC = settings.MANAGERS

def parking_ticket_appeal_form(request):
    if request.method == 'POST':
        form = ParkingTicketAppealForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            subject = "Parking Violation Appeal Request"
            send_mail(request, TO_LIST, subject, data['email'], "security/parking_ticket_appeal_email.html", data, BCC)
            return HttpResponseRedirect('/forms/security/success/')
    else:
        form = ParkingTicketAppealForm()
    return render_to_response('security/parking_ticket_appeal_form.html', {'form': form}, context_instance=RequestContext(request))
