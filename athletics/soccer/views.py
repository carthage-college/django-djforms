from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from djforms.athletics.soccer.forms import SoccerCampRegistrationForm

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

def camp_registration(request):
    if request.POST:
        form = SoccerCampRegistrationForm('0.99', request.POST) # charge for $0.99
        if form.is_valid():
            # logging shows the data you would likely store in a model
            r = form.gateway_response
            logging.debug("Transaction ID: %s" % (r.trans_id))
            logging.debug("Status: %s" % (r.status))
            logging.debug("Message: %s" % (r.message))
            return HttpResponseRedirect('/forms/athletics/soccer/camp/success/')
    else:
        form = SoccerCampRegistrationForm(None)

    return render_to_response('athletics/soccer/camp_registration.html',
                              {'form': form,},
                              context_instance=RequestContext(request))
