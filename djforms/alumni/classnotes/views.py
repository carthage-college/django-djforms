# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djforms.alumni.classnotes.forms import ContactForm
from djforms.alumni.classnotes.models import Contact
from djtools.utils.mail import send_mail


def contact(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = settings.ALUMNI_CLASSNOTES_EMAILS
    BCC = settings.MANAGERS

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if contact.email:
                email = contact.email
            subject = "[Alumni Class Notes] {0} {1}".format(
                contact.first_name, contact.last_name,
            )
            send_mail(
                request,
                TO_LIST,
                subject,
                email,
                'alumni/classnotes/email.html',
                contact,
                BCC,
            )
            return HttpResponseRedirect(reverse_lazy('classnotes_success'))
    else:
        form = ContactForm()
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/form.html',
        {'form': form, 'manager': manager},
    )


def archives(request, year=None):
    """Decade based archives."""
    if year:
        year = int(year)
    else:
        year = 2010

    ns = Contact.objects.exclude(pubstatus=False).exclude(
        category='Death Announcement',
    ).exclude(classnote__exact='None')
    notes = ns.filter(classyear__range=[year, year + 9]).order_by(
        '-classyear', '-created_at',
    )
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'year': year, 'manager': manager},
    )


def screenscrape(request):
    ns = Contact.objects.exclude(carthaginianstatus=True)
    notes = ns.order_by('classyear', 'last_name')
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'title': 'Carthaginian', 'manager': manager},
    )


def obits(request):
    obs = Contact.objects.filter(category='Death Announcement')
    notes = obs.order_by('-classyear', 'last_name')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'title': 'In Memoriam'},
    )
