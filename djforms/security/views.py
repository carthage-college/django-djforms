# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from djforms.security.forms import ParkingTicketAppealForm
from djtools.utils.mail import send_mail


def parking_ticket_appeal_form(request):
    """Parking ticket appear form view."""
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = [settings.SECURITY_PARKING_TICKET_APPEAL_EMAIL]

    if request.method == 'POST':
        form = ParkingTicketAppealForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            subject = "Parking Violation Appeal Request"
            send_mail(
                request,
                TO_LIST,
                subject,
                data['email'],
                'security/parking_ticket_appeal/email.html',
                data,
                [settings.SERVER_EMAIL],
            )
            return HttpResponseRedirect(
                reverse_lazy('parking_ticket_appeal_success'),
            )
    else:
        form = ParkingTicketAppealForm()

    return render(
        request,
        'security/parking_ticket_appeal/form.html',
        {'form': form},
    )
