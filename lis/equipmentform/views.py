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
            equip_list = '"'
            for i in cd['equipment']:
                equip_list += i.__str__() + ', '
            equip_list = equip_list[:-2] + '"'
            to = ['av@carthage.edu', cd['email']]
            bcc = settings.MANAGERS
            body =  cd['first_name'] + '\t' + cd['last_name'] + '\t' + \
                    cd['email'] + '\t' + \
                    cd['local_phone'] + '\t' + \
                    cd['status'] + '\t' + \
                    str(cd['date']) + '\t' + \
                    equip_list + '\t' + \
                    str(start_time) + '\t' + \
                    str(end_time) + '\t' + \
                    cd['title_of_event'] + '\t' + \
                    cd['department'] + '\t' + \
                    cd['course_number']
            email = EmailMessage("Equipment Reservation Request", body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/lis/success')
    else:
        form = EquipmentReserveForm()
    return render_to_response('lis/equipmentform/equipment_form.html', {'form': form}, context_instance=RequestContext(request))
