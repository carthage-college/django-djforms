# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from djforms.admissions.china.forms import InterestForm

from djtools.utils.mail import send_mail

import datetime


def interest_form(request):
    if request.method=='POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = settings.ADMISSIONS_CHINA_EMAIL_LIST

            BCC = settings.MANAGERS

            data = form.cleaned_data
            subject = "[Admissions][China] Prospective Student ({} {})".format(
                data['last_name'],data['first_name']
            )
            send_mail(
                request, TO_LIST, subject, data['email'],
                'admissions/china/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('admissions_china_success')
            )
    else:
        form = InterestForm()

    return render(
        request, 'admissions/china/form.html', { 'form': form, }
    )
