# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from djforms.communications.printrequest.forms import PrintRequestForm

from djtools.utils.mail import send_mail

REQ_ATTR = settings.REQUIRED_ATTRIBUTE


@login_required
def print_request(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = [settings.COMMUNICATIONS_PRINT_REQUEST_EMAIL]

    if request.method == 'POST':
        form = PrintRequestForm(
            request.POST,
            request.FILES,
            label_suffix='',
            use_required_attribute=REQ_ATTR,
        )
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.updated_by = request.user
            data.save()
            if not settings.DEBUG:
                TO_LIST.append(data.user.email)
                subject = '[Print request] {0}: {1}'.format(
                    data.project_name, data.date_created,
                ).encode('utf-8').strip()
                frum = data.user.email
                send_mail(
                    request,
                    TO_LIST,
                    subject,
                    frum,
                    'communications/printrequest/email.html',
                    data,
                    reply_to=[frum,],
                    bcc = [settings.MANAGERS[0][1],],
                )
                return HttpResponseRedirect(reverse('print_request_success'))
            else:
                return render(
                    request, 'communications/printrequest/email.html',
                    {'data': data},
                )
    else:
        form = PrintRequestForm(label_suffix='', use_required_attribute=REQ_ATTR)

    return render(
        request,
        'communications/printrequest/form.html',
        {'form': form},
    )
