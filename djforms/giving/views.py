from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djforms.giving.forms import *
from djforms.core.models import Promotion
from djforms.giving.models import DonationContact
from djforms.processors.forms import TrustCommerceForm as CreditCardForm

from djtools.fields import TODAY
from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

YEAR = TODAY.year
BRICK_PRICES = ["250","500",YEAR-2000+200,YEAR-2000+300]

from datetime import timedelta

import os


def giving_form(request, transaction, campaign=None):
    """
    multipurpose function to handle various types of donations
    """
    # recipients
    if settings.DEBUG or not settings.TC_LIVE:
        BCC = settings.MANAGERS
    else:
        BCC = settings.GIVING_DONATIONS_BCC

    status = None
    # subject of email
    SUBJECT = u"""Thank you, {} {}, for your donation to Carthage"""
    trans_cap = transaction.capitalize()
    # check for a campaign and obtain contact form
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
        ct_form_name = "{}{}ContactForm".format(
            campaign.slug.replace('-',' ').title().replace(' ',''),
            trans_cap
        )
    else:
        campaign = ""
        ct_form_name = trans_cap + "ContactForm"
    # order form
    or_form_name = trans_cap + "OrderForm"
    or_form = str_to_class(
        "djforms.giving.forms", or_form_name
    )
    ct_form = str_to_class(
        "djforms.giving.forms", ct_form_name
    )

    # just checking for bad requests
    if not or_form:
        raise Http404

    # there might not be a custom campaign form
    # so we just use the default contact form
    if campaign and not ct_form:
        ct_form_name = "{}{}ContactForm".format(
            settings.GIVING_DEFAULT_CONTACT_FORM,
            trans_cap
        )
        ct_form = str_to_class(
            "djforms.giving.forms", ct_form_name
        )

    years = None
    if request.POST:
        ct_form = str_to_class(
            "djforms.giving.forms", ct_form_name
        )(request.POST, prefix="ct")
        or_form = str_to_class(
            "djforms.giving.forms", or_form_name
        )(request.POST, prefix="or")
        cc_form = CreditCardForm(
            or_form, ct_form, request.POST
        )
        if ct_form.is_valid() and or_form.is_valid():
            contact = ct_form.save()
            or_data = or_form.save(commit=False)
            or_data.status = "In Process"
            or_data.operator = "DJForms%s" % trans_cap
            or_data.avs = 0
            or_data.auth = 'sale'
            # deal with commemorative brick options
            if transaction == "brick" and contact.class_of == str(YEAR):
                if or_data.total == 250:
                    or_data.total = BRICK_PRICES[2]
                elif or_data.total == 500:
                    or_data.total = BRICK_PRICES[3]
                else:
                    raise Http404
            # deal with payments if they have chosen to pledge
            if transaction != "brick" and request.POST.get("or-pledge") != "":
                #or_data.payments = request.POST["or-payments"]
                or_data.payments = 0
                or_data.auth = 'store'
                #or_data.grand_total = or_data.total
                #or_data.total = or_data.total / int(or_data.payments)
                or_data.cycle = "1m"
            else:
                or_data.payments = None
            if campaign:
                or_data.promotion = campaign
            or_data.save()
            contact.order.add(or_data)
            email = contact.email
            cc_form = CreditCardForm(
                or_data, contact, request.POST
            )
            if cc_form.is_valid():
                # save and update order
                r = cc_form.processor_response
                or_data.status = r.msg['status']
                or_data.transid = r.msg['transid']
                or_data.billingid = r.msg.get('billingid')
                or_data.cc_name = cc_form.name
                or_data.cc_4_digits = cc_form.card[-4:]
                or_data.save()
                # sendmail
                or_data.contact = contact
                data = {'order':or_data,'years':years}
                subject = SUBJECT.format(contact.first_name, contact.last_name)
                sent = send_mail(
                    request, [email,], subject, email,
                    'giving/%s_email.html' % transaction, data, BCC
                )
                or_data.send_mail = sent
                or_data.save()
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
                    or_data.status = "Form Invalid"
                or_data.cc_name = cc_form.name
                if cc_form.card:
                    or_data.cc_4_digits = cc_form.card[-4:]
                status = or_data.status
                or_data.save()
        #else:
        #    cc_form = CreditCardForm(None, request.POST)
        #    cc_form.is_valid()
    else:
        # order form
        init = {}
        if request.GET.get("amount"):
            try:
                # simple way to guard against malicious data
                init["total"] = "{0:.2f}".format(float(request.GET.get("amount")))
            except:
                pass
        or_form = str_to_class(
            "djforms.giving.forms", or_form_name
        )(prefix="or", initial=init)
        # contact form
        ct_form = str_to_class(
            "djforms.giving.forms", ct_form_name
        )(prefix="ct")
        # credit card
        cc_form = CreditCardForm()

    # build our template path
    template = 'giving/{}_form.html'.format(transaction)
    if campaign:
        temp = 'giving/campaigns/{}/{}_form.html'.format(
            campaign.slug,transaction
        )
        if os.path.isfile(os.path.join(settings.ROOT_DIR, "templates", temp)):
            template = temp
        else:
            template = 'giving/campaigns/{}/{}_form.html'.format(
                settings.GIVING_DEFAULT_CAMPAIGN, transaction
            )

    return render_to_response(
        template,
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

    # build our template path
    template = 'giving/{}_success.html'.format(transaction)
    if campaign:
        temp = 'giving/campaigns/{}/{}_success.html'.format(
            campaign.slug, transaction
        )
        if os.path.isfile(os.path.join(settings.ROOT_DIR, "templates", temp)):
            template = temp
        else:
            template = 'giving/campaigns/{}/{}_success.html'.format(
                settings.GIVING_DEFAULT_CAMPAIGN, transaction
            )

    return render_to_response(
        template,
        { 'campaign': campaign, },
        context_instance=RequestContext(request)
    )


def donors(request, slug=None):

    promo = None
    start_date = TODAY - timedelta(days=365)
    template = 'giving/donors.html'

    if slug:
        promo = get_object_or_404(Promotion, slug=slug)
        if slug == 'giving-day':
            const = '{}_START_DATE'.format(promo.slug.replace('-','_').upper())
            start_date = getattr(settings, const, None)

        # template
        temp = 'giving/campaigns/{}/donors.html'.format(promo.slug)
        if os.path.isfile(os.path.join(settings.ROOT_DIR, "templates", temp)):
            template = temp

    donors = DonationContact.objects.filter(anonymous=False).filter(
        order__time_stamp__gte=start_date
    ).filter(order__status__in=['approved','manual'])

    if slug and slug != 'giving-day':
        donors = donors.filter(order__promotion__slug=slug)

    return render_to_response(
        template, {
            'donors':donors, 'promo':promo, 'count':donors.count()
        }, context_instance=RequestContext(request)
    )


def promotion_ajax(request, slug):
    '''
    ajax request, returns HTML for dynamic display.
    accepts a campaign slug for identifying the Promotion() class object.
    '''
    promo = get_object_or_404(Promotion, slug=slug)

    return render_to_response(
        "giving/promotion_ajax.html",
        {"data":promo,},
        context_instance=RequestContext(request)
    )


@staff_member_required
def manager_cash(request):
    '''
    cash donation form
    '''

    if request.POST:
        ct_form = ManagerContactForm(request.POST, prefix="ct")
        or_form = ManagerOrderForm(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            # contact
            contact = ct_form.save(commit=False)
            contact.opt_in = 0
            contact.anonymous = 0
            contact.matching_company = 0
            contact.save()
            # order
            or_data = or_form.save(commit=False)
            or_data.status = "Manual"
            or_data.operator = "DJFormsCashDonation"
            or_data.avs = 0
            or_data.auth = 'cash'
            or_data.save()
            contact.order.add(or_data)
            # redirect
            return HttpResponseRedirect( reverse( 'giving_manager_success') )
    else:
        ct_form = ManagerContactForm(prefix="ct")
        or_form = ManagerOrderForm(prefix="or")

    return render_to_response(
        "giving/manager/cash_form.html",
        {'ct_form': ct_form, 'or_form':or_form,},
        context_instance=RequestContext(request)
    )

