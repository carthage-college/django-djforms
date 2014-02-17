# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djforms.admissions.china.forms import InterestForm
from djtools.utils.mail import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["admissions@carthage.edu","tkline@carthage.edu"]
BCC = settings.MANAGERS

def interest_form(request):
    if request.method=='POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = """[Admissions][China] Prospective Student (%s %s)""" % (
                data['last_name'],data['first_name']
            )
            send_mail(
                request, TO_LIST, subject, data['email'],
                "admissions/china/email.html", data, BCC
            )
            return HttpResponseRedirect('http://www.carthage.edu/china/success/')
    else:
        form = InterestForm()
    return render_to_response(
        "admissions/china/form.html",
        {
            "form": form,
        }, context_instance=RequestContext(request))
