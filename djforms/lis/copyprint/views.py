# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from djforms.lis.copyprint.forms import CardRequestForm

from djtools.utils.mail import send_mail


@login_required
def index(request):
    if request.method == 'POST':
        form = CardRequestForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [
                    settings.COPYPRINT_CARD_REQUEST_EMAIL,
                    data.user.email
                ]
            subject = 'Copy Print Card Request: {}, {} from {}'.format(
                data.user.last_name, data.user.first_name, data.entity_name
            )
            frum = data.user.email
            send_mail(
                request,
                TO_LIST,
                subject,
                frum,
                'lis/copyprint/email.html',
                data,
                reply_to=[frum,],
                bcc=[settings.MANAGERS[0][1],],
            )
            return HttpResponseRedirect(
                reverse_lazy('lis_success')
            )
    else:
        form = CardRequestForm()

    return render(
        request, 'lis/copyprint/form.html', {'form':form,}
    )
