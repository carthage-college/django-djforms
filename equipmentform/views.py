from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response 
from django.template import RequestContext

from djforms.equipmentform.forms import EquipmentReserveForm

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
            start_time = cd['start_time']
            #set up the equipment list
            equip_list = '\n'+'\n'
            for i in cd['equipment']:
                equip_list = equip_list + i.__str__() + '\n'
            to = ['awyma@carthage.edu', cd['email']]
            body =  'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' + \
                    'E-mail: ' + cd['email'] + '\n' + \
                    'Local Phone: ' + cd['local_phone'] + '\n' + \
                    'Status: ' + cd['status'] + '\n' + \
                    'Date Equipment is needed: ' + str(cd['date']) + '\n' + \
                    'Requested Equipment: ' + equip_list + '\n' + \
                    'Starting Time: ' +  + str(cd['start_time']) + '\n' + \
                    'Ending Time: ' +  str(cd['end_time']) + '\n' + \
                    'Title of event: ' + cd['title_of_event'] + '\n'+ \
                    'Department: ' + cd['department'] + '\n' + \
                    'Course Number: ' + cd['course_number'] + '\n'

            email = EmailMessage("Equipment Reservation Request", body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/reserve_complete')
    else:
        form = EquipmentReserveForm()
    return render_to_response('equipmentform/equipment_form.html', {'form': form}, context_instance=RequestContext(request))
