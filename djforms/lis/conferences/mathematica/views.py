from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.core.urlresolvers import reverse

from djforms.processors.forms import TrustCommerceForm as ProcessorForm
from djforms.lis.conferences.mathematica.forms import RegistrationOrderForm
from djforms.lis.conferences.mathematica.forms import RegistrationForm

from djtools.utils.mail import send_mail

def registration_form(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = ["mathematica@carthage.edu",]
    BCC = settings.MANAGERS

    if request.POST:
        email_template = "lis/conferences/mathematica/registration_email.html"
        form_reg = RegistrationForm(request.POST)
        form_ord = RegistrationOrderForm(request.POST)
        if form_reg.is_valid() and form_ord.is_valid():
            contact = form_reg.save()
            order = form_ord.save()
            order.operator = "DJFormsMathematicaReg"
            contact.order.add(order)
            form_proc = ProcessorForm(order, contact, request.POST)
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.cc_name = form_proc.name
                order.cc_4_digits = form_proc.card[-4:]
                order.save()
                order.contact = contact
                TO_LIST.append(contact.email)
                subject = "[LIS] Mathematica conference registration"
                send_mail(
                    request, TO_LIST, subject,
                    contact.email, email_template, order, BCC
                )
                return HttpResponseRedirect(
                    reverse('mathematica_registration_success')
                )
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = "Blocked"
                order.cc_name = form_proc.name
                if form_proc.card:
                    order.cc_4_digits = form_proc.card[-4:]
                order.save()
                if settings.DEBUG:
                    order.contact = contact
                    send_mail(
                        request, TO_LIST, subject,
                        contact.email, email_template, order, BCC
                    )
                else:
                    return HttpResponseRedirect(
                        reverse('mathematica_registration_success')
                    )
        else:
            form_proc = ProcessorForm(None, request.POST)
            form_proc.is_valid()
    else:
        form_reg = RegistrationForm()
        form_ord = RegistrationOrderForm(initial={'avs':False,'auth':'sale',})
        form_proc = ProcessorForm()

    return render_to_response(
        'lis/conferences/mathematica/registration_form.html',
        {
            'form_reg':form_reg,'form_ord':form_ord,'form_proc':form_proc
        },
        context_instance=RequestContext(request)
    )

def registration_success(request):
    return render_to_response(
        "lis/conferences/mathematica/registration_done.html",
        context_instance=RequestContext(request)
    )
