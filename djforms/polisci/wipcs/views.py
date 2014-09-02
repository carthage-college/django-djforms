from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.polisci.wipcs.forms import RegistrationContactForm
from djforms.polisci.wipcs.forms import RegistrationOrderForm
from djforms.processors.forms import TrustCommerceForm
from djtools.utils.mail import send_mail

def registration(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = ["vdillinger@carthage.edu",]
    BCC = settings.MANAGERS

    if request.POST:
        form_con = RegistrationContactForm(request.POST,request.FILES)
        form_ord = RegistrationOrderForm(request.POST)
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            order.operator = "DJ PoliSci: WIPCS"
            if contact.payment_method == "Credit Card":
                form_proc = TrustCommerceForm(order, contact, request.POST)
                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.cc_name = form_proc.name
                    order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
                    order.reg = contact
                    order.contact = contact
                    send_mail(
                        request, TO_LIST,
                        "[WIPCS] Conference Registration",
                        contact.email, "polisci/wipcs/email.html", order, BCC,
                        attach=True
                    )
                    return HttpResponseRedirect(
                        reverse('wipcs_registration_success')
                    )
                else:
                    r = form_proc.processor_response
                    if r:
                        order.status = r.status
                    else:
                        order.status = "Blocked"
                    order.cc_name = form_proc.name
                    if form_proc.card:
                        order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
            else:
                order.auth="COD"
                order.status="Pay later"
                order.save()
                contact.order.add(order)
                order.reg = contact
                order.contact = contact
                send_mail(
                    request, TO_LIST,
                    "[WIPCS] Conference Registration",
                    contact.email, "polisci/wipcs/email.html", order, BCC,
                    attach=True
                )
                return HttpResponseRedirect(
                    reverse('wipcs_registration_success')
                )
        else:
            if request.POST.get('payment_method') == "Credit Card":
                form_proc = TrustCommerceForm(None, request.POST)
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm()
    else:
        form_con = RegistrationContactForm()
        form_ord = RegistrationOrderForm(
            initial={'avs':False,'auth':'sale'}
        )
        form_proc = TrustCommerceForm()
    return render_to_response(
        'polisci/wipcs/form.html', {
            'form_con': form_con, 'form_ord':form_ord,
            'form_proc':form_proc
        }, context_instance=RequestContext(request))

