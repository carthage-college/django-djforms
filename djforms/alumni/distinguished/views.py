from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from djforms.alumni.distinguished.forms import NomineeForm, NominatorForm

from djtools.utils.mail import send_mail

import datetime


def nomination_form(request):
    if request.method == 'POST':
        nominee_form = NomineeForm(request.POST,prefix='nominee')
        nominator_form = NominatorForm(request.POST,prefix='nominator')
        if nominee_form.is_valid() and nominator_form.is_valid():
            data = {
                'nominee': nominee_form.cleaned_data,
                'nominator': nominator_form.cleaned_data
            }
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [settings.ALUMNI_OFFICE_EMAIL]
            subject = 'Distinguished Alumni Award Nomination: {}'.format(
                data['nominee']['name']
            )
            frum = data['nominator']['email']
            send_mail(
                request,
                TO_LIST,
                subject,
                frum,
                'alumni/distinguished/email.html',
                data,
                reply_to=[frum,],
                bcc=[settings.MANAGERS[0][1],],
            )
            return HttpResponseRedirect(
                reverse_lazy('distinguished_nomination_success')
            )
    else:
        nominee_form = NomineeForm(prefix='nominee')
        nominator_form = NominatorForm(prefix='nominator')

    return render(
        request,
        'alumni/distinguished/form.html',
        {'nominee_form':nominee_form,'nominator_form':nominator_form,}
    )
