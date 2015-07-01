from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404

from djforms.processors.forms import TrustCommerceForm as CreditCardForm
from djforms.giving.forms import *
from djforms.core.models import Promotion
from djtools.utils.convert import str_to_class
from djtools.utils.mail import send_mail
from djtools.fields import TODAY

YEAR = TODAY.year
BRICK_PRICES = ["150","500",YEAR-2000+100,YEAR-2000+300]

import logging
logger = logging.getLogger(__name__)

def giving_form(request, transaction, campaign=None):
    """
    multipurpose function to handle various types of donations
    """
    # recipients
    if settings.DEBUG or not settings.TC_LIVE:
        BCC = settings.MANAGERS
    else:
        BCC = settings.GIVING_DONATIONS_BCC

    trans_cap = transaction.capitalize()
    ct_form_name = trans_cap + "ContactForm"
    or_form_name = trans_cap + "OrderForm"
    or_form = str_to_class(
        "djforms.giving.forms", or_form_name
    )
    ct_form = str_to_class(
        "djforms.giving.forms", ct_form_name
    )
    # just checking for bad requests
    if not or_form or not ct_form:
        raise Http404
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
    else:
        campaign = ""
    status = None
    years = None
    if request.POST:
        ct_form = str_to_class(
            "djforms.giving.forms", ct_form_name
        )(request.POST, prefix="ct")
        or_form = str_to_class(
            "djforms.giving.forms", or_form_name
        )(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            contact = ct_form.save()
            or_data = or_form.save(commit=False)
            or_data.status = "In Process"
            or_data.operator = "DJForms%s" % trans_cap
            if transaction == "brick" and contact.class_of == str(YEAR):
                if or_data.total == 150:
                    or_data.total = BRICK_PRICES[2]
                elif or_data.total == 500:
                    or_data.total = BRICK_PRICES[3]
                else:
                    raise Http404
            or_data.save()
            logger.debug("or_data = {}".format(or_data.__dict__))
            contact.order.add(or_data)
            email = contact.email
            cc_form = CreditCardForm(
                or_data, contact, request.POST, prefix="cc"
            )
            if cc_form.is_valid():
                # save and update order
                r = cc_form.processor_response
                if transaction == "pledge":
                    # deal with payments
                    years = str( int(or_data.payments) / 12 )
                    if or_data.cycle != "1m":
                        or_data.payments = str(
                            int(or_data.payments) / int(or_data.cycle[:-1])
                        )
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
                subject = "Thank you, %s %s, for your donation to Carthage" % (
                    contact.first_name,contact.last_name
                )
                send_mail(
                    request, [email,], subject, email,
                    'giving/%s_email.html' % transaction, data, BCC
                )
                # redirect
                if campaign:
                    url = reverse(
                        'giving_success_campaign',
                        args=[transaction,campaign.slug]
                    )
                else:
                    url = reverse(
                        'giving_success_generic',
                        args=[transaction]
                    )
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
                    logger.debug("cc = {}".format(cc_form.__dict__))
                    or_data.contact = contact
                    data = {'order':or_data,'campaign':campaign,'years':years,}
                    subject = "Thank you, %s %s, for your donation to Carthage" % (
                        contact.first_name,contact.last_name
                    )
                    send_mail(
                        request, [email,], subject, email,
                        'giving/%s_email.html' % transaction, data, BCC
                    )
        else:
            cc_form = CreditCardForm(None, request.POST, prefix="cc")
            cc_form.is_valid()
    else:
        initial = {'avs':False,'auth':'sale'}
        if transaction == "pledge":
            initial = {'cycle':"1m",'avs':False,'auth':'store',}

        # order form
        or_form = str_to_class(
            "djforms.giving.forms", or_form_name
        )(prefix="or", initial=initial)
        # contact form
        ct_form = str_to_class(
            "djforms.giving.forms", ct_form_name
        )(prefix="ct")
        # credit card
        cc_form = CreditCardForm(prefix="cc")

    return render_to_response(
        'giving/%s_form.html' % transaction,
        {
            'ct_form': ct_form, 'or_form': or_form, 'form_proc': cc_form,
            'status': status, 'campaign': campaign,'year':str(YEAR)
        },
        context_instance=RequestContext(request)
    )

def giving_success(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)

    return render_to_response(
        'giving/%s_success.html' % transaction,
        { 'campaign': campaign, },
        context_instance=RequestContext(request)
    )
