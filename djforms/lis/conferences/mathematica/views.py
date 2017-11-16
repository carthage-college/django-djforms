from django.conf import settings
from django.shortcuts import render
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
        TO_LIST = list(settings.LIS_MATHEMATICA_REGISTRATION_EMAIL)
    BCC = settings.MANAGERS

    if request.POST:
        email_template = 'lis/conferences/mathematica/registration_email.html'
        subject = '[LIS] Mathematica conference registration'
        form_reg = RegistrationForm(request.POST)
        form_ord = RegistrationOrderForm(request.POST)
        if form_reg.is_valid() and form_ord.is_valid():
            contact = form_reg.save()
            order = form_ord.save()
            order.operator = 'DJFormsMathematicaReg'
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
                sent = send_mail(
                    request, TO_LIST, subject,
                    contact.email, email_template, order, BCC
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(
                    reverse('mathematica_registration_success')
                )
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = 'Form Invalid'
                order.cc_name = form_proc.name
                if form_proc.card:
                    order.cc_4_digits = form_proc.card[-4:]
                order.save()
        else:
            form_proc = ProcessorForm(None, request.POST)
            form_proc.is_valid()
    else:
        form_reg = RegistrationForm()
        form_ord = RegistrationOrderForm(initial={'avs':False,'auth':'sale',})
        form_proc = ProcessorForm()

    return render(
        request,
        'lis/conferences/mathematica/registration_form.html',
        {
            'form_reg':form_reg,'form_ord':form_ord,'form_proc':form_proc
        }
    )

def registration_success(request):
    return render(
        request, 'lis/conferences/mathematica/registration_done.html'
    )
