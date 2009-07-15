from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response 
from djforms.roomform.reserve.forms import RoomReserveForm
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
            #set up the hours an minutes values accordingly
            start_hours = (cd['start_time'] / 3600).__str__()
            start_minutes = (cd['start_time'] / 60 % 60).__str__()
            end_hours = (cd['end_time'] / 3600).__str__()
            end_minutes = (cd['end_time'] / 60 % 60).__str__()
            #we gotta add the zero to the front if they equal 5 or 0
            if start_minutes == '0':
                start_minutes = '00'
                end_minutes = '00'
            if start_minutes == '5':
                start_minutes = '05'
                end_minutes = '05'
            if cd['room'] in AV_ROOMS:
                send_mail(
                    "Room Reservation Request, " + cd['room'],
                    
                    'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' +
                    'E-mail: ' + cd['email'] + '\n' +
                    'Local Phone: ' + cd['local_phone'] + '\n' +
                    'Status: ' + cd['status'] + '\n' +
                    'Date requested: ' + cd['date'].__str__() + '\n' +
                    'Starting Time: ' + start_hours +':'+ start_minutes + ' ' + cd['start_time_meridiem'] + '\n' +
                    'Ending Time: ' +  end_hours +':'+ end_minutes + ' ' + cd['end_time_meridiem'] + '\n' +
                    'Building and Room: ' + cd['room'] + '\n' +
                    'Title of event: ' + cd['title_of_event'] + '\n'+
                    'Department: ' + cd['department'] + '\n' +
                    'Course Number: ' + cd['course_number'] + '\n' +
                    'Additional Dates for this room at this time:  ' + cd['additional_requests'] + '\n' +
                    'Special needs and Comments: ' + cd['comments'] + '\n',
                    
                    cd['email'],
                    #av@carthage.edu
                    ['ngromiuk@carthage.edu', cd['email'],],
                )
            else:
                send_mail(
                    "Room Reservation Request, " + cd['room'],
                    
                    'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' +
                    'E-mail: ' + cd['email'] + '\n' +
                    'Local Phone: ' + cd['local_phone'] + '\n' +
                    'Status: ' + cd['status'] + '\n' +
                    'Date requested: ' + cd['date'].__str__() + '\n' +
                    'Starting Time: ' + start_hours +':'+ start_minutes + ' ' + cd['start_time_meridiem'] + '\n' +
                    'Ending Time: ' +  end_hours +':'+ end_minutes + ' ' + cd['end_time_meridiem'] + '\n' +
                    'Building and Room: ' + cd['room'] + '\n' +
                    'Title of event: ' + cd['title_of_event'] + '\n'+
                    'Department: ' + cd['department'] + '\n' +
                    'Course Number: ' + cd['course_number'] + '\n' +
                    'Additional Dates for this room at this time:  ' + cd['additional_requests'] + '\n' +
                    'Special needs and Comments: ' + cd['comments'] + '\n',
                    
                    cd['email'],
                    #av@carthage.edu
                    ['ngromiuk@carthage.edu', cd['email'],],
                )
            return HttpResponseRedirect('/reserve_complete')
    else:
        form = RoomReserveForm(
            initial={'first_name': 'Enter first name',
                    'last_name': 'Enter last name',
                    'email': 'Enter e-mail address',
                    'local_phone': 'Enter phone number'},
        )
    return render_to_response('roomform/room_form.html', {'form': form})