from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from djforms.lis.conferences.course_ference.forms import *
from djforms.processors.forms import TrustCommerceForm
from djtools.utils.mail import send_mail

import os

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["ezitron@carthage.edu",]
BCC = settings.MANAGERS

def registration_form(request, reg_type):
    # try/catch works as 404 detector and GET initialization for forms
    try:
        form_con = eval(reg_type.capitalize() + "ContactForm")()
        form_ord = eval(reg_type.capitalize() + "OrderForm")(initial={'avs':False,'auth':'sale',})
        email_template = "lis/conferences/course_ference/%s/email.html" % reg_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", email_template))
        form_proc = TrustCommerceForm()
    except:
        raise Http404

    if request.POST:
        form_con = eval(reg_type.capitalize() + "ContactForm")(request.POST)
        form_ord = eval(reg_type.capitalize() + "OrderForm")(request.POST)
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            order.operator = "LIS: Course-Ference"
            contact.order.add(order)
            form_proc = TrustCommerceForm(order, contact, request.POST)
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.save()
                order.contact = contact
                TO_LIST.append(contact.email)
                send_mail(request, TO_LIST, "[LIS] Course-Ference registration: %s" % reg_type, contact.email, email_template % reg_type, order, BCC)
                return HttpResponseRedirect(reverse('course_ference_registration_success'))
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = "Blocked"
                order.save()
                if settings.DEBUG:
                    order.contact = contact
                    send_mail(request, TO_LIST, "[LIS] Course-Ference registration: %s" % reg_type, contact.email, email_template % reg_type, order, BCC)
                    return HttpResponseRedirect(reverse('course_ference_registration_success'))
        else:
            form_proc = TrustCommerceForm(None, request.POST)
            form_proc.is_valid()

    return render_to_response('lis/conferences/course_ference/%s/form.html' % reg_type,
                              {'form_con': form_con, 'form_ord':form_ord, 'form_proc':form_proc, 'reg_type':reg_type,},
                              context_instance=RequestContext(request))

