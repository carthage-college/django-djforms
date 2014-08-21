from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.core.urlresolvers import reverse

from djforms.processors.forms import TrustCommerceForm as ProcessorForm
from djforms.lis.conferences.course_ference.forms import *
from djforms.lis.conferences.course_ference.models import CourseFerenceAttender

from djtools.utils.mail import send_mail
from json import dumps

import os

def registration_form(request, reg_type):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = ["nextgenlibraries@carthage.edu",]
    BCC = settings.MANAGERS

    # try/catch works as 404 detector and GET initialization for forms
    try:
        form_con = eval(reg_type.capitalize() + "ContactForm")()
        form_ord = eval(reg_type.capitalize() + "OrderForm")(initial={'avs':False,'auth':'sale',})
        email_template = "lis/conferences/course_ference/%s/email.html" % reg_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", email_template))
        form_proc = ProcessorForm()
    except:
        raise Http404
    # second contact form for attender guest
    guest = False
    if reg_type == "attender":
        form_con2 = AttenderContactForm2(prefix="guest")
    else:
        form_con2 = None

    if request.POST:
        form_con = eval(reg_type.capitalize() + "ContactForm")(request.POST)
        form_ord = eval(reg_type.capitalize() + "OrderForm")(request.POST)
        # guest form for attenders
        if form_con2:
            form_con2 = AttenderContactForm2(request.POST, prefix="guest")
            if form_con2.is_valid():
                guest = True
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            order.operator = "LIS: Course-Ference"
            contact.order.add(order)
            form_proc = ProcessorForm(order, contact, request.POST)
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.cc_name = form_proc.name
                order.cc_4_digits = form_proc.card[-4:]
                order.save()
                # save guest object if attender form & guest form is valid
                if guest:
                    guest = form_con2.save()
                    guest.order.add(order)
                    guest.save()
                order.contact = contact
                TO_LIST.append(contact.email)
                # save guest to order object for email data
                order.guest = guest
                send_mail(
                    request, TO_LIST,
                    "[LIS] Course-Ference registration: %s" % reg_type,
                    contact.email, email_template, order, BCC
                )
                return HttpResponseRedirect(
                    reverse('course_ference_registration_success',
                        kwargs={
                            'reg_type': reg_type,
                        },
                    )
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
                        request, TO_LIST, "[LIS] Course-Ference registration: %s" % reg_type,
                        contact.email, email_template, order, BCC
                    )
                    """
                    return HttpResponseRedirect(
                        reverse('course_ference_registration_success',
                            kwargs={
                                'reg_type': reg_type,
                            },
                        )
                    )
                    """
        else:
            form_proc = ProcessorForm(None, request.POST)
            form_proc.is_valid()

    return render_to_response(
        'lis/conferences/course_ference/%s/form.html' % reg_type,
        {
            'form_con':form_con,'form_con2':form_con2,'form_ord':form_ord,
            'form_proc':form_proc,'reg_type':reg_type,'guest':guest
        },
        context_instance=RequestContext(request)
    )

def registration_success(request, reg_type):
    try:
        template = "lis/conferences/course_ference/%s/done.html" % reg_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", template))
    except:
        raise Http404

    return render_to_response(
        template, context_instance=RequestContext(request)
    )


def json_map_data(request):
    cfa = CourseFerenceAttender.objects.filter(longitude__isnull=False)
    jay = '{"markers":['
    for c in cfa:
        if c.longitude and c.latitude:
            # json encode
            jay += '{"id":"%s","lat":"%s","long":"%s","creator":"Carthage College","created":1310499032,' % (c.id,c.longitude,c.latitude)
            jay += '"name":"%s"},' % c.affiliation
    jay = jay[:-1] + "]}"
    return HttpResponse(jay, mimetype="text/plain; charset=utf-8")

