from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.athletics.soccer.forms import SoccerCampRegistrationForm
from djforms.processors.models import Contact, Order
from djforms.processors.forms import ContactForm, TrustCommerceForm
from djtools.utils.mail import send_mail

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["sdomin@carthage.edu",]
BCC = settings.MANAGERS

def camp_registration(request):
    status = None
    if request.POST:
        form_reg = SoccerCampRegistrationForm(request.POST)
        form_con = ContactForm(request.POST)
        if form_reg.is_valid() and form_con.is_valid():
            reg_data = form_reg.cleaned_data
            con_data = form_con.cleaned_data
            # we might have a record for 'contact' so we use get_or_create() method
            contact, created = Contact.objects.get_or_create(first_name=con_data['first_name'],last_name=con_data['last_name'],email=con_data['email'],phone=con_data['phone'],address1=con_data['address1'],address2=con_data['address2'],city=con_data['city'],state=con_data['state'],postal_code=con_data['postal_code'],country="US")
            # calc amount
            if reg_data["amount"] == "Full amount":
                total = reg_data['reg_fee']
            else:
                if int(reg_data['reg_fee']) < 195:
                    total = 50
                else:
                    total = 200
            # credit card payment
            if reg_data['payment_method'] == "Credit Card":
                order = Order(total=total,auth="sale",status="In Process",operator="Soccer Camp")
                form_proc = TrustCommerceForm(order, contact, request.POST)
                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.save()
                    contact.order.add(order)
                    order.reg = reg_data
                    send_mail(request, TO_LIST, "Soccer camp registration", contact.email, "athletics/soccer/camp_registration_email.html", order, BCC)
                    return HttpResponseRedirect(reverse('soccer_camp_success'))
                else:
                    r = form_proc.processor_response
                    if r:
                        order.status = r.status
                    else:
                        order.status = "Blocked"
                    order.save()
                    contact.order.add(order)
                    status = order.status
            else:
                order = Order(total=total,status="Pay later")
                order.reg = reg_data
                order.contact = contact
                send_mail(request, TO_LIST, "Soccer camp registration", contact.email, "athletics/soccer/camp_registration_email.html", order, BCC)
                return HttpResponseRedirect(reverse('soccer_camp_success'))
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
                              {'form_reg': form_reg, 'form_con':form_con, 'form_proc':form_proc,'status':status,},
                              context_instance=RequestContext(request))

