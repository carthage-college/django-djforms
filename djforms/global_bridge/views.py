from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.global_bridge import BCC, TO_LIST
from djforms.global_bridge.forms import RegistrationForm, RegistrationOrderForm

from djforms.processors.models import Contact, Order
from djforms.processors.forms import TrustCommerceForm

from djtools.utils.mail import send_mail

def index(request):
    status = None
    msg = None
    if request.POST:
        form_reg = RegistrationForm(request.POST)
        form_ord = RegistrationOrderForm(request.POST)
        if form_reg.is_valid() and form_ord.is_valid():
            contact = form_reg.save()
            data_ord = form_ord.cleaned_data
            # credit card payment
            if contact.payment_method == "Credit Card":
                order = Order(
                    total=data_ord["total"],auth="sale",status="In Process",
                    operator="GlobalBridgeReg"
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
                    sent = send_mail(
                        request, TO_LIST,
                        "Global Bridge registration",
                        contact.email,
                        "global_bridge/registration_email.html",
                        order, BCC
                    )
                    order.send_mail = sent
                    order.save()
                    return HttpResponseRedirect(
                        reverse('global_bridge_registration_success')
                    )
                else:
                    r = form_proc.processor_response
                    if r:
                        order.status = r.status
                    else:
                        order.status = "Form Invalid"
                    order.cc_name = form_proc.name
                    if form_proc.card:
                        order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
                    status = order.status
                    order.reg = contact
            else:
                order = Order(
                    total=data_ord["total"], auth="COD", status="Pay later",
                    operator="DJFormsGlobalBrigReg"
                )
                order.save()
                contact.order.add(order)
                order.reg = contact
                sent = send_mail(
                    request, TO_LIST,
                    "Global Bridge registration",
                    contact.email,
                    "global_bridge/registration_email.html",
                    order, BCC
                )
                order.send_mail = sent
                order.save()
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
        initial = {'avs':False,'auth':'sale'}
        form_reg = RegistrationForm()
        form_ord = RegistrationOrderForm(initial=initial)
        form_proc = TrustCommerceForm()
    return render_to_response(
        'global_bridge/registration_form.html',
        {
            'form_reg': form_reg,'form_proc':form_proc,'form_ord': form_ord,
            'status':status,'msg':msg,
        }, context_instance=RequestContext(request)
    )
