from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect

from djforms.processors.forms import SubscriptionOrderForm as OrderForm, ContactForm, TrustCommerceForm as CreditCardForm
from djforms.giving.models import Campaign
"""
import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG,)
#logging.debug("response: %s" % r.__dict__)
"""

def subscription(request, campaign=""):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Campaign, slug=campaign)
    status = None
    if request.POST:
        ct_form = ContactForm(request.POST, prefix="ct")
        or_form = OrderForm(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            ct_data = ct_form.save()
            or_data = or_form.save(commit=False)
            or_data.contact = ct_data
            or_data.status = "In Process"
            or_data.save()
            cc_form = CreditCardForm(or_data, request.POST, prefix="cc")
            if cc_form.is_valid():
                # save and update order
                cc_data = cc_form.cleaned_data
                r = cc_form.processor_response
                or_data.status = r.msg['status']
                or_data.billingid = r.msg['billingid']
                or_data.transid = r.msg['transid']
                or_data.save()
                # sendmail
                bcc = settings.MANAGERS
                recipient_list = ["larry@carthage.edu",]
                #recipient_list = ["lhansen@carthage.edu","fleisky@carthage.edu",]
                t = loader.get_template('giving/subscription_email.html')
                c = RequestContext(request, {'order':or_data,'campaign':campaign,})
                email = EmailMessage(("[Subscription Donation] %s %s" % (or_data.contact.first_name,or_data.contact.last_name)), t.render(c), or_data.contact.email, recipient_list, bcc, headers = {'Reply-To': or_data.contact.email,'From': or_data.contact.email})
                email.content_subtype = "html"
                email.send(fail_silently=True)
                # redirect
                url = '/forms/giving/subscription/success/%s' % campaign
                return HttpResponseRedirect(url)
            else:
                r = cc_form.processor_response
                status = r.status
                if r:
                    or_data.status = status
                else:
                    or_data.status = "Blocked"
                or_data.save()
        else:
            cc_form = CreditCardForm(None, request.POST, prefix="cc")
            cc_form.is_valid()
    else:
        ct_form = ContactForm(prefix="ct")
        or_form = OrderForm(prefix="or", initial={'cycle': "1m", 'avs':False,'auth':'store',})
        cc_form = CreditCardForm(prefix="cc")

    return render_to_response('giving/subscription_form.html',
                              {'ct_form': ct_form, 'or_form': or_form, 'cc_form': cc_form, 'status': status, 'campaign': campaign,},
                              context_instance=RequestContext(request))

def subscription_success(request, campaign=""):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Campaign, slug=campaign)

    return render_to_response('giving/subscription_success.html',
                              { 'campaign': campaign, },
                              context_instance=RequestContext(request))
