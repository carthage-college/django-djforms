from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from djforms.athletics.soccer.forms import SoccerCampRegistrationForm
from djforms.processors.models import Contact, Order
from djforms.processors.forms import ContactForm, TrustCommerceForm

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG,)

def camp_registration(request):
    if request.POST:
        form_reg = SoccerCampRegistrationForm(request.POST)
        form_con = ContactForm(request.POST)
        if form_reg.is_valid() and form_con.is_valid():
            reg_data = form_reg.cleaned_data
            if reg_data['payment_method'] == "Credit Card":
                con_data = form_con.cleaned_data
                # we might have a record for 'contact' so we use get_or_create() method
                contact, created = Contact.objects.get_or_create(first_name=con_data['first_name'], last_name=con_data['last_name'], email=con_data['email'], phone=con_data['phone'],address1=con_data['address1'],address2=con_data['address2'],city=con_data['city'],state=con_data['state'],postal_code=con_data['postal_code'])
                if request.POST["amount"] == "Full amount":
                    total = reg_data['reg_fee']
                else:
                    if int(reg_data['reg_fee']) <= 195:
                        total = 50
                    else:
                        total = 200
                order = Order(contact=contact,total=total,status="In Process")
                form_proc = TrustCommerceForm(order, request.POST)
                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.auth = "sale"
                    order.save()
                    return HttpResponseRedirect('http://%s/forms/athletics/soccer/camp/success/' % settings.SERVER_URL)
                else:
                    r = form_proc.processor_response
                    status = r.status
                    if r:
                        order.status = status
                    else:
                        order.status = "Blocked"
                    order.save()
                    form_proc = TrustCommerceForm(None, request.POST)
                    form_proc.is_valid()
            else:
                return HttpResponseRedirect('http://%s/forms/athletics/soccer/camp/success/' % settings.SERVER_URL)
        else:
            if request.POST.get('payment_method') == "Credit Card":
                form_proc = TrustCommerceForm(None, request.POST)
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm()
    else:
        form_reg = SoccerCampRegistrationForm()
        form_con = ContactForm()
        form_proc = TrustCommerceForm()
    return render_to_response('athletics/soccer/camp_registration.html',
                              {'form_reg': form_reg, 'form_con':form_con, 'form_proc':form_proc,},
                              context_instance=RequestContext(request))
