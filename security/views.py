from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import EmailMessage

from djforms.security.forms import ParkingTicketAppealForm

def parking_ticket_appeal_form(request):
    if request.method == 'POST':
        form = ParkingTicketAppealForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            to = ['parking@carthage.edu', cd['email']]
            #to = ['larry@carthage.edu', cd['email']]
            bcc = settings.MANAGERS
            body =  'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' + \
                    'E-mail: ' + cd['email'] + '\n' + \
                    'Carthage ID#: ' + cd['carthage_id'] + '\n' + \
                    'Residency Status: ' + cd['residency_status'].name + '\n' + \
                    'Vehicle Make: ' + cd['vehicle_make'] + '\n' + \
                    'Vehicle Model: ' + cd['vehicle_model'] + '\n' + \
                    'License Plate: ' + cd['license_plate'] + '\n' + \
                    'State: ' +  cd['state'] + '\n' + \
                    'Permit Type: ' + cd['permit_type'].name + '\n'+ \
                    'Permit Number: ' + cd['permit_number'] + '\n' + \
                    'Citation Number: ' + cd['citation_number'] + '\n'+ \
                    'Appeal Comments: ' +  '\n' + cd['appeal_box'] + '\n'
            email = EmailMessage("Parking Violation Appeal Request", body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/security/success')
    else:
        form = ParkingTicketAppealForm()
    return render_to_response('security/parking_ticket_appeal_form.html', {'form': form}, context_instance=RequestContext(request))
