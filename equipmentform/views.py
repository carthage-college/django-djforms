from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response 
from djforms.equipmentform.reserve.forms import EquipmentReserveForm
from datetime import date
    
def equipment_reserve(request):
    if request.method == 'POST':
        form = EquipmentReserveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #set up end time and end time meridiem
            #end time is four hours after the start time so just add 4 hours, but its a little tricky
            #1. check if the hour is == 12 if not its going to be < 12 (The time will never be greater than 12 because of the dropdown menu)
            #2. if = 12 just the hour will be 4 and the meridiem stays the same
            #3. else (< 12) add 4, then if >= 12 subtract twelve and swap sign
            #4. convert the time to seconds
            end_time = cd['end_time']
            end_time_hours = int(cd['start_time_hours'])
            end_time_minutes = int(cd['start_time_minutes'])
            end_time_meridiem = cd['start_time_meridiem']
            if end_time_hours == 12:
                end_time_hours = 4
            else:
                end_time_hours = end_time_hours + 4
                if end_time_hours >= 12:
                    if end_time_hours > 12:
                        end_time_hours = end_time_hours - 12
                    if end_time_meridiem == 'a.m.':
                        end_time_meridiem = 'p.m.'
                    else:
                        end_time_meridiem = 'a.m.'
            #set the time to the proper amount of seconds
            end_time = (end_time_hours * 3600) + ( end_time_minutes * 60 )
            #set up the hours an minutes values accordingly
            start_hours = (cd['start_time'] / 3600).__str__()
            start_minutes = (cd['start_time'] / 60 % 60).__str__()
            end_hours = (end_time / 3600).__str__()
            end_minutes = (end_time / 60 % 60).__str__()
            #we gotta add the zero to the front if they equal 5 or 0
            if start_minutes == '0':
                start_minutes = '00'
                end_minutes = '00'
            if start_minutes == '5':
                start_minutes = '05'
                end_minutes = '05'
            #set up the equipment list
            equip_list = '\n'+'\n'
            for i in cd['equipment']:
                equip_list = equip_list + i.__str__() + '\n'
                
            send_mail(
                "Equipment Reservation Request",
                
                'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' +
                'E-mail: ' + cd['email'] + '\n' +
                'Local Phone: ' + cd['local_phone'] + '\n' +
                'Status: ' + cd['status'] + '\n' +
                'Date Equipment is needed: ' + cd['date'].__str__() + '\n' +
                'Requested Equipment: ' + equip_list + '\n' +
                'Starting Time: ' + start_hours +':'+ start_minutes + ' ' + cd['start_time_meridiem'] + '\n' +
                'Ending Time: ' +  end_hours +':'+ end_minutes + ' ' + end_time_meridiem + '\n' +
                'Title of event: ' + cd['title_of_event'] + '\n'+
                'Department: ' + cd['department'] + '\n' +
                'Course Number: ' + cd['course_number'] + '\n',
                
                cd['email'],
                #mmazanet@carthage.edu
                ['ngromiuk@carthage.edu', cd['email'],],
            )
            return HttpResponseRedirect('/reserve_complete')
    else:
        form = EquipmentReserveForm()
    return render_to_response('equipmentform/equipment_form.html', {'form': form})