# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from djforms.athletics.soccer import BCC
from djforms.athletics.soccer import INSURANCE_TO_LIST
from djforms.athletics.soccer import TO_LIST
from djforms.processors.models import Order
from djforms.processors.forms import TrustCommerceForm
from djforms.athletics.soccer.forms import SoccerCampBalanceForm
from djforms.athletics.soccer.forms import SoccerCampBalanceOrderForm
from djforms.athletics.soccer.forms import SoccerCampRegistrationForm
from djforms.athletics.soccer.forms import SoccerCampInsuranceCardForm
from djtools.utils.mail import send_mail


def camp_registration(request):
    """Soccer camp registration form."""
    status = None
    msg = None
    if request.POST:
        form_reg = SoccerCampRegistrationForm(request.POST)
        if form_reg.is_valid():
            contact = form_reg.save()
            # calc amount
            fee = contact.reg_fee
            if fee[0] == '$':
                fee = fee[1:]
            if contact.amount == 'Full amount':
                total = int(float(fee))
            else:
                if int(float(fee)) <= 225:
                    total = 50
                else:
                    total = 200
            # credit card payment
            if contact.payment_method == 'Credit Card':
                order = Order(
                    total=total,
                    auth='sale',
                    status='In Process',
                    operator='DJSoccerCamp',
                )
                form_proc = TrustCommerceForm(
                    order, contact, request.POST,
                    use_required_attribute=False
                )
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
                        request,
                        TO_LIST,
                        'Soccer camp registration',
                        contact.email,
                        'athletics/soccer/camp_registration_email.html',
                        order,
                        BCC,
                    )
                    order.send_mail = sent
                    order.save()
                    return HttpResponseRedirect(reverse('soccer_camp_success'))
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
                    status = order.status
                    order.reg = contact
                    sent = send_mail(
                        request,
                        TO_LIST,
                        '[{0}] Soccer camp registration'.format(status),
                        contact.email,
                        'athletics/soccer/camp_registration_email.html',
                        order,
                        BCC,
                    )
                    order.send_mail = sent
                    order.save()
            else:
                order = Order(
                    total=total,
                    auth='COD',
                    status='Pay later',
                    operator='DJSoccerCamp',
                )
                order.save()
                contact.order.add(order)
                order.reg = contact
                sent = send_mail(
                    request,
                    TO_LIST,
                    "Soccer camp registration",
                    contact.email,
                    'athletics/soccer/camp_registration_email.html',
                    order,
                    BCC,
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(reverse('soccer_camp_success'))
        else:
            if request.POST.get('payment_method') == 'Credit Card':
                form_proc = TrustCommerceForm(
                    None,
                    request.POST,
                    use_required_attribute=False,
                )
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm(use_required_attribute=False)
    else:
        form_reg = SoccerCampRegistrationForm()
        form_proc = TrustCommerceForm(use_required_attribute=False)

    return render(
        request,
        'athletics/soccer/camp_registration.html',
        {'form_reg': form_reg, 'form_proc': form_proc, 'status': status},
    )


def insurance_card(request):
    """Upload insurance card form."""
    if request.POST:
        form = SoccerCampInsuranceCardForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            subject = u"[Insurance card]: {}, {}".format(
                data['last_name'], data['first_name']
            )
            send_mail(
                request, INSURANCE_TO_LIST,
                subject, data['email'],
                'athletics/soccer/camp_insurance_card_email.html',
                data, BCC, attach=True
            )
            return HttpResponseRedirect(
                reverse('soccer_camp_insurance_card_success')
            )
    else:
        form = SoccerCampInsuranceCardForm()

    return render(
        request, 'athletics/soccer/camp_insurance_card_form.html',
        {'form': form,}
    )


def camp_balance(request):
    """Allow folks to pay your registration balance."""
    status = None
    msg = None
    if request.POST:
        form_bal = SoccerCampBalanceForm(
            request.POST, use_required_attribute=False,
        )
        form_ord = SoccerCampBalanceOrderForm(
            request.POST, label_suffix='', use_required_attribute=False,
        )
        if form_bal.is_valid() and form_ord.is_valid():
            order = form_ord.save(commit=False)
            order.auth='sale'
            order.status='In Process'
            order.operator='DJSoccerCamp'
            order.save()
            contact = form_bal.save()
            form_proc = TrustCommerceForm(
                order,
                contact,
                request.POST,
                use_required_attribute=False,
            )
            subject = u"[Soccer Camp Balance paid]: {0}, {1}".format(
                contact.last_name, contact.first_name,
            )
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.cc_name = form_proc.name
                order.cc_4_digits = form_proc.card[-4:]
                order.save()
                contact.order.add(order)
                order.reg = contact
                # send mail to user and athletics folks
                to = {'user': [contact.email], 'athletics': INSURANCE_TO_LIST}
                for dest in ['user', 'athletics']:
                    send_mail(
                        request,
                        to[dest],
                        subject,
                        contact.email,
                        'athletics/soccer/camp_balance_{0}.html'.format(dest),
                        order,
                        BCC,
                    )
                return HttpResponseRedirect(
                    reverse('soccer_camp_balance_success')
                )
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
                order.reg = contact
                send_mail(
                    request,
                    INSURANCE_TO_LIST,
                    subject,
                    contact.email,
                    'athletics/soccer/camp_balance_athletics.html',
                    order,
                    BCC,
                )
        else:
            form_proc = TrustCommerceForm(
                None, request.POST, use_required_attribute=False,
            )
            form_proc.is_valid()
    else:
        form_bal = SoccerCampBalanceForm(use_required_attribute=False)
        form_ord = SoccerCampBalanceOrderForm(use_required_attribute=False)
        form_proc = TrustCommerceForm(use_required_attribute=False)

    return render(
        request,
        'athletics/soccer/camp_balance.html', {
            'form_bal': form_bal,
            'form_proc': form_proc,
            'form_ord': form_ord,
            'status':status,
        },
    )
