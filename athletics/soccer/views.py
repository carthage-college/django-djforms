from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from djforms.athletics.soccer.forms import SoccerCampRegistrationForm, SoccerCampProcessorForm

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

def camp_registration(request):
    if request.POST:
        form_reg = SoccerCampRegistrationForm(request.POST)
        form_proc = SoccerCampProcessorForm(request.POST)
        if form_reg.is_valid():
            reg_data = form_reg.cleaned_data
            if reg_data['payment_method'] == "Credit Card" and form_proc.is_valid():
                proc_data = form_proc.cleaned_data
            # logging shows the data you would likely store in a model
            r = form.gateway_response
            logging.debug("Transaction ID: %s" % (r.trans_id))
            logging.debug("Status: %s" % (r.status))
            logging.debug("Message: %s" % (r.message))
            return HttpResponseRedirect('/forms/athletics/soccer/camp/success/')
    else:
        form_reg = SoccerCampRegistrationForm(None)
        form_proc = SoccerCampProcessorForm(None)

    return render_to_response('athletics/soccer/camp_registration.html',
                              {'form_reg': form_reg, 'form_proc':form_proc,},
                              context_instance=RequestContext(request))
