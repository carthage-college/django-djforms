from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response, get_object_or_404

from djtools.utils.mail import send_mail
from djforms.polisci.mun.forms import ModelUnitedNationsRegistrationForm
from djforms.polisci.mun.forms import ModelUnitedNationsCountriesForm

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["kvega@carthage.edu",]
BCC = settings.MANAGERS

def registration_form(request):
    if request.method=='POST':
        form = ModelUnitedNationsRegistrationForm(request.POST)
        c_form = ModelUnitedNationsCountriesForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            obj = form.cleaned_data
            data = {'object':obj,'dele':c_form.cleaned_data,}
            subject = "[Model United Nations Registration] %s of %s" % (
                obj['faculty_advisor'],obj['school_name']
            )
            send_mail(
                request, TO_LIST, subject, obj['email'],
                "polisci/mun/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("model_un_registration_success")
            )
    else:
        form = ModelUnitedNationsRegistrationForm()
        c_form = ModelUnitedNationsCountriesForm()
    return render_to_response(
        "polisci/mun/form.html",
        {"form": form,"c_form":c_form,},
        context_instance=RequestContext(request)
    )
