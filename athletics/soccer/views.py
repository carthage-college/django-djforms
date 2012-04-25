from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from djforms.athletics.soccer.forms import SoccerCampRegistrationForm, SoccerCampProcessorForm
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

def camp_registration(request):
    if request.POST:
        form_reg = SoccerCampRegistrationForm(request.POST)
        form_con = ContactForm(request.POST)
        if form_reg.is_valid() and form_con.is_valid():
            reg_data = form_reg.cleaned_data
            if reg_data['payment_method'] == "Credit Card":
                contact = form_con.save()
                order = Order(contact=contact,total=request.POST["amount"],status="In Process")
                form_proc = SoccerCampProcessorForm(order, request.POST)
                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.billingid = r.msg['billingid']
                    order.transid = r.msg['transid']
                    order.save()
                    return HttpResponseRedirect('http://%s/forms/athletics/soccer/camp/success/' % settings.SERVER_URL)
                else:
                    form_proc = SoccerCampProcessorForm(None, request.POST)
                    form_proc.is_valid()
            else:
                return HttpResponseRedirect('http://%s/forms/athletics/soccer/camp/success/' % settings.SERVER_URL)
        else:
            if request.POST.get('payment_method') == "Credit Card":
                form_proc = SoccerCampProcessorForm(None, request.POST)
                form_proc.is_valid()
            else:
                form_proc = SoccerCampProcessorForm()
    else:
        form_reg = SoccerCampRegistrationForm()
        form_con = ContactForm()
        form_proc = SoccerCampProcessorForm()
    return render_to_response('athletics/soccer/camp_registration.html',
                              {'form_reg': form_reg, 'form_con':form_con, 'form_proc':form_proc,},
                              context_instance=RequestContext(request))
