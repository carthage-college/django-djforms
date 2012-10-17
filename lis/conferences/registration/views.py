from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.lis.conferences.registration.forms import RegistrationContactForm, RegistrationOrderForm
from djforms.processors.forms import TrustCommerceForm
from djforms.core.views import send_mail

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["ezitron@carthage.edu",]
BCC = settings.MANAGERS

def registration_form(request):
    if request.POST:
        form_con = RegistrationContactForm(request.POST)
        form_ord = RegistrationOrderForm(request.POST)
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            form_proc = TrustCommerceForm(order, contact, request.POST)
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.save()
                contact.order.add(order)
                send_mail(request, TO_LIST, "[LIS] Conference Registration", contact.email, "lis/conferences/registration/email.html", order, BCC)
                return HttpResponseRedirect(reverse('conference_registration_success'))
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = "Blocked"
                order.save()
                contact.order.add(order)
        else:
            form_proc = TrustCommerceForm(None, request.POST)
            form_proc.is_valid()
    else:
        form_con = RegistrationContactForm()
        form_ord = RegistrationOrderForm()
        form_proc = TrustCommerceForm()
    return render_to_response('lis/conferences/registration/form.html',
                              {'form_con': form_con, 'form_ord':form_ord, 'form_proc':form_proc,},
                              context_instance=RequestContext(request))

