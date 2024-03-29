# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from djforms.security.forms import AnonymousReportForm
from djforms.security.forms import ParkingTicketAppealForm
from djtools.utils.mail import send_mail


def anonymous_report(request):
    """anonymous report form view."""
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = [settings.SECURITY_REPORT_EMAIL]
    if request.method == 'POST':
        form = AnonymousReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = "Anonymous Report"
            send_mail(
                request,
                TO_LIST,
                subject,
                TO_LIST[0],
                'security/anonymous_report/email.html',
                data,
                [settings.SERVER_EMAIL],
            )
            return HttpResponseRedirect(
                reverse_lazy('anonymous_report_success'),
            )
    else:
        form = AnonymousReportForm()

    return render(
        request,
        'security/anonymous_report/form.html',
        {'form': form},
    )


def parking_ticket_appeal(request):
    """Parking ticket appeal form view."""
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
