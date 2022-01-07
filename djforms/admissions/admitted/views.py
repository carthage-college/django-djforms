from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from djforms.admissions.admitted.forms import ChanceForm

from djtools.utils.mail import send_mail

import datetime


def chance_form(request):
    if settings.DEBUG:
        to_list = [settings.SERVER_EMAIL]
    else:
        to_list = settings.ADMISSIONS_ADMITTED_EMAIL_LIST

    prospect_status = None
    if request.GET.keys():
        prospect_status = list(request.GET.keys())[0]
    if request.method=='POST':
        form = ChanceForm(request.POST)
        if form.is_valid():
            data = form.save()
            if data.gpa_scale == '100':
                data.adjusted_gpa = (float(data.gpa) - 60)/10
            else:
                data.adjusted_gpa = (float(data.gpa) * 4) / float(data.gpa_scale)
            data.save()
            subject = "Carthage, will I be admitted? ({0})".format(
                data.first_name,
            )
            send_mail(
                request,
                to_list,
                subject,
                data.email,
                'admissions/admitted/email.html',
                data,
                settings.ADMISSIONS_BCC,
            )
            return HttpResponseRedirect(
                reverse_lazy('admitted_success')
            )
        else:
            prospect_status = request.POST.get('prospect_status')
    else:
        form = ChanceForm()

    return render(
        request, 'admissions/admitted/form.html',
        {
            'form': form,
            'prospect_status':prospect_status
        }
    )
