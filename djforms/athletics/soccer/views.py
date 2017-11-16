from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse

from djforms.athletics.soccer import BCC, INSURANCE_TO_LIST, TO_LIST
from djforms.processors.models import Contact, Order
from djforms.processors.forms import TrustCommerceForm
from djforms.athletics.soccer.forms import SoccerCampRegistrationForm
from djforms.athletics.soccer.forms import SoccerCampInsuranceCardForm

from djtools.utils.mail import send_mail


def camp_registration(request):

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
                    total=total,auth='sale',status='In Process',
                    operator='DJSoccerCamp'
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
                        request, TO_LIST, 'Soccer camp registration',
                        contact.email,
                        'athletics/soccer/camp_registration_email.html',
                        order, BCC
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
                        request, TO_LIST,
                        '[{}] Soccer camp registration'.format(status),
                        contact.email,
                        'athletics/soccer/camp_registration_email.html',
                        order, BCC
                    )
                    order.send_mail = sent
                    order.save()
            else:
                order = Order(
                    total=total,auth='COD',status='Pay later',
                    operator='DJSoccerCamp'
                )
                order.save()
                contact.order.add(order)
                order.reg = contact
                sent = send_mail(
                    request, TO_LIST, "Soccer camp registration",
                    contact.email,
                    'athletics/soccer/camp_registration_email.html', order, BCC
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(reverse('soccer_camp_success'))
        else:
            if request.POST.get('payment_method') == 'Credit Card':
                form_proc = TrustCommerceForm(None, request.POST)
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm()
    else:
        form_reg = SoccerCampRegistrationForm()
        form_proc = TrustCommerceForm()

    return render(
        request, 'athletics/soccer/camp_registration.html',
        {
            'form_reg': form_reg,'form_proc':form_proc,
            'status':status,'msg':msg,
        }
    )


def insurance_card(request):
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
