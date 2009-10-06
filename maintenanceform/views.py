from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from djforms.maintenanceform.forms import MaintenanceEVSForm
from djforms.maintenanceform.models import MaintenanceRequest

def data_entered(request):
    return render_to_response('jobpost/data_entered.html')
    
def maintenance_form(request):
    return render_to_response('jobpost/data_entered.html')
