from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.polisci.mun.forms import ModelUnitedNationsRegistrationForm, ModelUnitedNationsCountriesForm

def registration_form(request):
    form = ModelUnitedNationsRegistrationForm()
    c_form = ModelUnitedNationsCountriesForm()
    return render_to_response("polisci/mun/registration_form.html", {"form": form,"c_form":c_form,}, context_instance=RequestContext(request))
