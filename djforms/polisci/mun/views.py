from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djtools.utils.mail import send_mail
from djforms.polisci.mun.forms import AttenderForm, CountryForm

def registration(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = [
            "jroberg@carthage.edu"
            "ncottrell@carthage.edu",
        ]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form_cont = AttenderForm(request.POST, prefix="cont")
        form_pais = CountryForm(request.POST, prefix="pais")
        if form_cont.is_valid() and form_pais.is_valid():
            contact = form_cont.cleaned_data
            data = {'object':contact,'dele':form_pais.cleaned_data}
            subject = "[Model United Nations Registration] %s %s of %s" % (
                contact["first_name"], contact["last_name"],
                contact["school_name"]
            )
            send_mail(
                request, TO_LIST, subject, contact['email'],
                "polisci/mun/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("model_united_nations_success")
            )
    else:
        form_cont = AttenderForm(prefix="cont")
        form_pais = CountryForm(prefix="pais")
    return render_to_response(
        "polisci/mun/form.html",
        {"form_cont":form_cont,"form_pais":form_pais},
        context_instance=RequestContext(request)
    )
