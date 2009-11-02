from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from djforms.maintenanceform.forms import MaintenanceEVSForm
from djforms.maintenanceform.models import MaintenanceRequest

def data_entered(request):
    return render_to_response('jobpost/data_entered.html')
    
def maintenance_evs_form(request):
    if request.method == 'POST':
        form = MaintenanceEVSForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/forms/maint-evs-form/data_entered')
    else:
        form = PostFormWithoutHidden(instance=post)
    return render_to_response("maint-evs-form/maintenance_evs_form.html", {"form": form})
