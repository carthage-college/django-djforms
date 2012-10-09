from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.core.views import send_mail
from djforms.polisci.mun.forms import ModelUnitedNationsRegistrationForm, ModelUnitedNationsCountriesForm

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["vmartinez1@carthage.edu",]
BCC = settings.MANAGERS

def registration_form(request):
    if request.method=='POST':
        form = ModelUnitedNationsRegistrationForm(request.POST)
        c_form = ModelUnitedNationsCountriesForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            obj = form.cleaned_data
            data = {'object':obj,'dele':c_form.cleaned_data,}
            subject = "[Model United Nations Registration] %s of %s" % (obj['faculty_advisor'],obj['school_name'])
            send_mail(request, TO_LIST, subject, obj['email'], "polisci/mun/registration_email.html", data, BCC)
            return HttpResponseRedirect('/forms/political-science/model-united-nations/success/')
    else:
        form = ModelUnitedNationsRegistrationForm()
        c_form = ModelUnitedNationsCountriesForm()
    return render_to_response("polisci/mun/registration_form.html", {"form": form,"c_form":c_form,}, context_instance=RequestContext(request))
