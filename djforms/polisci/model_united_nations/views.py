from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response, get_object_or_404

from djforms.polisci.model_united_nations.forms import AttenderForm
from djforms.polisci.model_united_nations.forms import CountryForm

from djtools.utils.mail import send_mail

def registration(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = ["vdillinger@carthage.edu",]
    BCC = settings.MANAGERS
    if request.method=='POST':
        form_cont = AttenderForm(request.POST, prefix="cont")
        form_pais = CountryForm(request.POST, prefix="pais")
        if form_cont.is_valid() and form_pais.is_valid():
            contact = form_cont.save()
            paises = form_pais.cleaned_data
            contact.delegation_1 = paises["delegation_1"]
            contact.delegation_2 = paises["delegation_2"]
            contact.delegation_3 = paises["delegation_3"]
            contact.delegation_4 = paises["delegation_4"]
            contact.delegation_5 = paises["delegation_5"]
            contact.save()
            data = {'object':contact}
            subject = "[Model United Nations Registration] %s %s of %s" % (
                contact.first_name, contact.last_name, contact.school_name
            )
            send_mail(
                request, TO_LIST, subject, contact.email,
                "polisci/model_united_nations/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("model_united_nations_success")
            )
    else:
        form_cont = AttenderForm(prefix="cont")
        form_pais = CountryForm(prefix="pais")
    return render_to_response(
        "polisci/model_united_nations/form.html", {
            "form_cont":form_cont,"form_pais":form_pais,
        },
        context_instance=RequestContext(request)
    )
