from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.polisci.mun.forms import ModelUnitedNationsRegistrationForm, ModelUnitedNationsCountriesForm

def registration_form(request):
    if request.method=='POST':
        form = ModelUnitedNationsRegistrationForm(request.POST)
        c_form = ModelUnitedNationsCountriesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            dele = c_form.is_valid()
            bcc = settings.MANAGERS
            recipient_list = ["jroberg@carthage.edu",]
            t = loader.get_template('polisci/mun/registration_email.html')
            c = RequestContext(request, {'object':data,'dele':c_form.cleaned_data,})
            email = EmailMessage(("[Model United Nations Registration] %s of %s" % (data['faculty_advisor'],data['school_name'])), t.render(c), data['email'], recipient_list, bcc, headers = {'Reply-To': data['email'],'From': data['email']})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/political-science/model-united-nations/success/')
    else:
        form = ModelUnitedNationsRegistrationForm()
        c_form = ModelUnitedNationsCountriesForm()
    return render_to_response("polisci/mun/registration_form.html", {"form": form,"c_form":c_form,}, context_instance=RequestContext(request))
