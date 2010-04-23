from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djforms.lis.equipmentform.forms import EquipmentReserveForm

from datetime import date

def equipment_reserve(request):
    if request.method == 'POST':
        form = EquipmentReserveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            end_time = cd['end_time']
            start_time = cd['start_time']
            #set up the equipment list
            equip_list = '\n'+'\n'
            for i in cd['equipment']:
                equip_list = equip_list + i.__str__() + '\n'
            to = ['av@carthage.edu', cd['email']]
            bcc = settings.MANAGERS
            body =  'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' + \
                    'E-mail: ' + cd['email'] + '\n' + \
                    'Local Phone: ' + cd['local_phone'] + '\n' + \
                    'Status: ' + cd['status'] + '\n' + \
                    'Date Equipment is needed: ' + str(cd['date']) + '\n' + \
                    'Requested Equipment: ' + equip_list + '\n' + \
                    'Starting Time: ' +  str(start_time) + '\n' + \
                    'Ending Time: ' +  str(end_time) + '\n' + \
                    'Title of event: ' + cd['title_of_event'] + '\n' + \
                    'Department: ' + cd['department'] + '\n' + \
                    'Course Number: ' + cd['course_number'] + '\n'
            email = EmailMessage("Equipment Reservation Request", body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/lis/success')
    else:
        form = EquipmentReserveForm()
    return render_to_response('lis/equipmentform/equipment_form.html', {'form': form}, context_instance=RequestContext(request))
