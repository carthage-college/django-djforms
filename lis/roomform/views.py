from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from djforms.lis.roomform.forms import RoomReserveForm
from datetime import date

AV_ROOMS=[  'Hedberg Library 105',
            'Hedberg Library 106',
            'Hedberg Library 107',
            'Hedberg Library 108',
            'Hedberg Library 109',
            'Hedberg Library 162',
            'Hedberg Library 163',
            'Hedberg Library 164',]

def room_reserve(request):
    if request.method == 'POST':
        form = RoomReserveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            to = ['mmazanet@carthage.edu',cd['email']]
            bcc = settings.MANAGERS
            if cd['room'] in AV_ROOMS:
                to = ['av@carthage.edu',cd['email']]
            body =  'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' +\
                    'E-mail: ' + cd['email'] + '\n' +\
                    'Local Phone: ' + cd['local_phone'] + '\n' +\
                    'Status: ' + cd['status'] + '\n' +\
                    'Date requested: ' + str(cd['date']) + '\n' +\
                    'Starting Time: ' + str(cd['start_time']) + '\n' +\
                    'Ending Time: ' +  str(cd['end_time']) + '\n' +\
                    'Building and Room: ' + cd['room'] + '\n' +\
                    'Title of event: ' + cd['title_of_event'] + '\n'+\
                    'Department: ' + cd['department'] + '\n' +\
                    'Course Number: ' + cd['course_number'] + '\n' +\
                    'Additional requests:  ' + cd['additional_requests'] + '\n' +\
                    'Special needs and Comments: ' + cd['comments'] + '\n'

            email = EmailMessage("Room Reservation Request: %s" % cd['room'], body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/lis/success')
    else:
        form = RoomReserveForm()
    return render_to_response('lis/roomform/room_form.html', {'form': form}, context_instance=RequestContext(request))
