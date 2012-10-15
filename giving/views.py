from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404

from djforms.processors.forms import TrustCommerceForm as CreditCardForm
from djforms.giving.forms import *
from djforms.core.models import Promotion
from djforms.core.views import send_mail

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["lpieta@carthage.edu","lhansen@carthage.edu",]
BCC = settings.MANAGERS

def giving_form(request, transaction, campaign=None):
    """
    multipurpose method to handle various types of donations
    """
    or_form_name = transaction.capitalize() + "OrderForm"
    try:
        form = eval(or_form_name)()
    except:
        raise Http404
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
    status = None
    if request.POST:
        ct_form = DonationContactForm(request.POST, prefix="ct")
        or_form = eval(or_form_name)(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            contact = ct_form.save()
            or_data = or_form.save(commit=False)
            or_data.status = "In Process"
            or_data.operator = "Giving: %s" % transaction
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
                else:
                    years = None
                or_data.status = r.msg['status']
                or_data.billingid = r.msg['billingid']
                or_data.transid = r.msg['transid']
                if campaign:
                    or_data.promotion = campaign
                or_data.save()
                # sendmail
                data = {'order':or_data,'campaign':campaign,'years':years,}
                subject = "[pledge Donation] %s %s" % (contact.first_name,contact.last_name)
                email = contact.email
                TO_LIST.append(email)
                send_mail(request, TO_LIST, subject, email, 'giving/%s_email.html' % transaction, data, BCC)
                # redirect
                slug = ""
                if campaign:
                    slug = campaign.slug
                url = 'http://www.carthage.edu/forms/giving/pledge/success/%s' % slug
                return HttpResponseRedirect(url)
            else:
                r = cc_form.processor_response
                if r:
                    or_data.status = r.status
                else:
                    or_data.status = "Blocked"
                status = or_data.status
                or_data.save()
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

    return render_to_response('giving/%s_form.html' % transaction,
                              {'ct_form': ct_form, 'or_form': or_form, 'cc_form': cc_form, 'status': status, 'campaign': campaign,},
                              context_instance=RequestContext(request))

def giving_success(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)

    return render_to_response('giving/%s_success.html' % transaction,
                              { 'campaign': campaign, },
                              context_instance=RequestContext(request))
