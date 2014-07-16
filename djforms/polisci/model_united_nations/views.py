from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response, get_object_or_404

from djforms.polisci.model_united_nations.forms import AttenderForm, OrderForm
from djforms.polisci.model_united_nations.forms import CountryForm
from djforms.processors.forms import TrustCommerceForm as CreditCardForm

from djtools.utils.mail import send_mail

def registration(request):
    if settings.DEBUG:
        TO_LIST = ["larry@carthage.edu",]
    else:
        TO_LIST = ["kvega@carthage.edu",]
    BCC = settings.MANAGERS
    if request.method=='POST':
        form_cont = AttenderForm(request.POST, prefix="cont")
        form_pais = CountryForm(request.POST, prefix="pais")
        form_ordr = OrderForm(request.POST, prefix="ordr")
        if form_cont.is_valid() and form_ordr.is_valid() and \
          form_pais.is_valid():
            form_proc = CreditCardForm(form_ordr, contact, request.POST)
            obj = form.cleaned_data
            data = {'object':obj,'dele':c_form.cleaned_data,}
            subject = "[Model United Nations Registration] %s of %s" % (
                obj['faculty_advisor'],obj['school_name']
            )
            send_mail(
                request, TO_LIST, subject, obj['email'],
                "polisci/model_united_nations/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("model_united_nations_success")
            )
        else:
            if request.POST.get('payment_method') == "Credit Card":
                form_proc = CreditCardForm(None, request.POST, prefix="proc")
                form_proc.is_valid()
            else:
                form_proc = CreditCardForm(prefix="proc")
    else:
        form_cont = AttenderForm(prefix="cont")
        form_pais = CountryForm(prefix="pais")
        form_ordr = OrderForm(prefix="ordr")
        form_proc = CreditCardForm(prefix="proc")
    return render_to_response(
        "polisci/model_united_nations/form.html", {
            "form_cont":form_cont,"form_pais":form_pais,
            "form_ordr":form_ordr, "form_proc":form_proc
        },
        context_instance=RequestContext(request)
    )
