from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djtools.utils.mail import send_mail
from djforms.polisci.mun.forms import AttenderForm, CountryForm

def registration(request):
    if settings.DEBUG:
        TO_LIST = ["larry@carthage.edu"]
    else:
        TO_LIST = ["vdillinger@carthage.edu"]

    if request.method=='POST':
        form_cont = AttenderForm(request.POST, prefix="cont")
        form_pais = CountryForm(request.POST, prefix="pais")
        if form_cont.is_valid():
            obj = form_cont.cleaned_data
            data = {'object':obj,'dele':form_pais.cleaned_data}
            subject = "[Model United Nations Registration] %s of %s" % (
                obj['faculty_advisor'],obj['school_name']
            )
            send_mail(
                request, TO_LIST, subject, obj['email'],
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
        "form_cont":form_cont,"form_pais":form_pais,
        context_instance=RequestContext(request)
    )
