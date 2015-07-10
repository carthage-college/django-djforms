from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.global_bridge import BCC, TO_LIST, REG_FEE
from djforms.global_bridge.forms import RegistrationForm

from djforms.processors.models import Contact, Order
from djforms.processors.forms import TrustCommerceForm

from djtools.utils.mail import send_mail

def index(request):
    status = None
    msg = None
    if request.POST:
        form_reg = RegistrationForm(request.POST)
        if form_reg.is_valid():
            contact = form_reg.save()
            # credit card payment
            if contact.payment_method == "Credit Card":
                order = Order(
                    total=REG_FEE,auth="sale",status="In Process",
                    operator="DJFormsGlobalBrigReg"
                )
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
                    send_mail(
                        request, TO_LIST,
                        "Global Bridge registration",
                        contact.email,
                        "global_bridge/registration_email.html",
                        order, BCC
                    )
                    return HttpResponseRedirect(
                        reverse('global_bridge_registration_success')
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
                    status = order.status
                    order.reg = contact
                    send_mail(
                        request, TO_LIST,
                        "[{}] Global Bridge registration".format(status),
                        contact.email,
                        "global_bridge/registration_email.html",
                        order, BCC
                    )
            else:
                order = Order(
                    total=REG_FEE,auth="COD",status="Pay later",
                    operator="DJFormsGlobalBrigReg"
                )
                order.save()
                contact.order.add(order)
                order.reg = contact
                send_mail(
                    request, TO_LIST,
                    "Global Bridge registration",
                    contact.email,
                    "global_bridge/registration_email.html",
                    order, BCC
                )
                return HttpResponseRedirect(
                    reverse('global_bridge_registration_success')
                )
        else:
            if request.POST.get('payment_method') == "Credit Card":
                form_proc = TrustCommerceForm(None, request.POST)
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm()
    else:
        form_reg = RegistrationForm()
        form_proc = TrustCommerceForm()
    return render_to_response(
        'global_bridge/registration_form.html',
        {
            'form_reg': form_reg,'form_proc':form_proc,
            'status':status,'msg':msg,
        }, context_instance=RequestContext(request)
    )
