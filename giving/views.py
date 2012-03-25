from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from djforms.giving.forms import SubscriptionForm

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

def subscription(request, campaign=None):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # logging shows the data you would likely store in a model
            #r = form.gateway_response
            #logging.debug("Transaction ID: %s" % (r.trans_id))
            #logging.debug("Status: %s" % (r.status))
            #logging.debug("Message: %s" % (r.message))
            if campaign:
                campaign = "/%s/" % campaign
            else:
                campaign = "/"
            return HttpResponseRedirect('/forms/giving/subscription%ssuccess/') % campaign
    else:
        form = SubscriptionForm(None)

    return render_to_response('giving/subscription_form.html',
                              {'form': form,},
                              context_instance=RequestContext(request))
