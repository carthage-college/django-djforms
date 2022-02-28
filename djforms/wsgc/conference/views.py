# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from djforms.wsgc.conference.forms import RegistrationForm
from djforms.wsgc.conference.forms import RegistrationOrderForm
from djforms.processors.forms import TrustCommerceForm
from djtools.utils.mail import send_mail


def form(request):
    """Registration form."""
    required_attribute = settings.REQUIRED_ATTRIBUTE
    if request.POST:
        form_con = RegistrationForm(
            request.POST,
            use_required_attribute=required_attribute,
        )
        form_ord = RegistrationOrderForm(
            request.POST,
            use_required_attribute=required_attribute,
        )
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            contact.order.add(order)
            order.operator = settings.WSGC_OPERATOR
            order.reg = contact
            order.contact = contact
            reg = order.contact.registration_type.split('|')
            order.contact.registration_type = '{0} (${1})'.format(reg[0],reg[1])
            if contact.payment_method == 'Credit Card':
                order.total = float(order.total) + (float(order.total) * .03)
                form_proc = TrustCommerceForm(
                    order, contact, request.POST, use_required_attribute=False,
                )
                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.cc_name = form_proc.name
                    order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    sent = send_mail(
                        request,
                        TO_LIST,
                        "[WSGC] Conference Registration",
                        contact.email,
                        'wsgc/conference/email.html',
                        order,
                        BCC,
                    )
                    order.send_mail = sent
                    order.save()
                    return HttpResponseRedirect(reverse('wsgc_conference_success'))
                else:
                    r = form_proc.processor_response
                    if r:
                        order.status = r.status
                    else:
                        order.status = 'Form Invalid'
                    order.cc_name = form_proc.name
                    if form_proc.card:
                        order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
            else:
                order.auth='COD'
                order.status='Pay later'
                order.save()
                contact.order.add(order)
                order.reg = contact
                order.contact = contact
                sent = send_mail(
                    request,
                    TO_LIST,
                    "[WSGC] Conference Registration",
                    contact.email,
                    'wsgc/conference/email.html',
                    order,
                    BCC,
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(reverse('wsgc_conference_success'))
        else:
            if request.POST.get('payment_method') == 'Credit Card':
                form_proc = TrustCommerceForm(
                    None, request.POST, use_required_attribute=False,
                )
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm(use_required_attribute=False)
    else:
        form_con = RegistrationForm(
            use_required_attribute=required_attribute,
        )
        form_ord = RegistrationOrderForm(
            initial={'avs':False,'auth':'sale'},
            use_required_attribute=required_attribute,
        )
        form_proc = TrustCommerceForm(use_required_attribute=False)

    return render(
        request,
        'wsgc/conference/form.html',
        {
            'form_con': form_con,
            'form_ord': form_ord,
            'form_proc': form_proc,
        },
    )
