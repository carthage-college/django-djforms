from django.conf import settings
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404

from djforms.processors.forms import TrustCommerceForm as CreditCardForm
from djforms.giving.forms import *
from djforms.core.models import Promotion
from djtools.utils.mail import send_mail

def giving_form(request, transaction, campaign=None):
    """
    multipurpose method to handle various types of donations
    """
    # recipients
    TO_LIST = []
    if settings.DEBUG:
        BCC = settings.MANAGERS
    else:
        BCC = [settings.SERVER_EMAIL,
            "lpiela@carthage.edu","lhansen@carthage.edu",
            "hkeller@carthage.edu","arobillard@carthage.edu"
        ]

    trans_cap = transaction.capitalize()
    or_form_name = trans_cap + "OrderForm"
    try:
        form = eval(or_form_name)()
    except:
        raise Http404
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
    else:
        campaign = ""
    status = None
    years = None
    if request.POST:
        ct_form = DonationContactForm(request.POST, prefix="ct")
        or_form = eval(or_form_name)(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            contact = ct_form.save()
            email = contact.email
            or_data = or_form.save(commit=False)
            or_data.status = "In Process"
            if campaign:
                or_data.operator = ("DJ%s%s" % (trans_cap,campaign.slug.capitalize()))[:20]
            else:
                or_data.operator = "DJForms%s" % trans_cap
            or_data.save()
            contact.order.add(or_data)
            cc_form = CreditCardForm(or_data, contact, request.POST, prefix="cc")
            if cc_form.is_valid():
                # save and update order
                r = cc_form.processor_response
                if transaction == "pledge":
                    # deal with payments
                    years = str( int(or_data.payments) / 12 )
                    if or_data.cycle != "1m":
                        or_data.payments = str( int(or_data.payments) / int(or_data.cycle[:-1]) )
                or_data.status = r.msg['status']
                or_data.transid = r.msg['transid']
                or_data.billingid = r.msg.get('billingid')
                or_data.cc_name = cc_form.name
                or_data.cc_4_digits = cc_form.card[-4:]
                if campaign:
                    or_data.promotion = campaign
                or_data.save()
                # sendmail
                or_data.contact = contact
                data = {'order':or_data,'campaign':campaign,'years':years,}
                subject = "Thank you, %s %s, for your donation to Carthage" % (contact.first_name,contact.last_name)
                TO_LIST.append(email)
                send_mail(
                    request, TO_LIST, subject, email,
                    'giving/%s_email.html' % transaction, data, BCC
                )
                # redirect
                slug = ""
                if campaign:
                    slug = campaign.slug
                url = 'http://www.carthage.edu/forms/giving/%s/success/%s' % (transaction, slug)
                return HttpResponseRedirect(url)
            else:
                r = cc_form.processor_response
                if r:
                    or_data.status = r.status
                else:
                    or_data.status = "Blocked"
                or_data.cc_name = cc_form.name
                if cc_form.card:
                    or_data.cc_4_digits = cc_form.card[-4:]
                status = or_data.status
                or_data.save()
                if settings.DEBUG:
                    or_data.contact = contact
                    data = {'order':or_data,'campaign':campaign,'years':years,}
                    subject = "Thank you, %s %s, for your donation to Carthage" % (
                        contact.first_name,contact.last_name
                    )
                    send_mail(
                        request, TO_LIST, subject, email,
                        'giving/%s_email.html' % transaction, data, BCC
                    )
        else:
            cc_form = CreditCardForm(None, request.POST, prefix="cc")
            cc_form.is_valid()
    else:
        if transaction == "pledge":
            initial = {'cycle':"1m",'avs':False,'auth':'store',}
        else:
            initial = {'avs':False,'auth':'sale',}
        ct_form = DonationContactForm(prefix="ct")
        or_form = eval(or_form_name)(prefix="or", initial=initial)
        cc_form = CreditCardForm(prefix="cc")

    return render_to_response(
        'giving/%s_form.html' % transaction,
        {
            'ct_form': ct_form, 'or_form': or_form, 'form_proc': cc_form,
            'status': status, 'campaign': campaign,
        },
        context_instance=RequestContext(request)
    )

def giving_success(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)

    return render_to_response('giving/%s_success.html' % transaction,
                              { 'campaign': campaign, },
                              context_instance=RequestContext(request))
