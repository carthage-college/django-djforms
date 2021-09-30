# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djforms.music.ensembles.choral.forms import CandidateForm
from djforms.music.ensembles.choral.forms import ManagerForm
from djtools.utils.mail import send_mail


@login_required
def candidate(request):
    """Choral tryout form."""
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            # set the time slot active state to False
            candidate.time_slot.active = False
            candidate.time_slot.save()
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [candidate.user.email]
            send_mail(
                request, TO_LIST,
                '[Choral Tryout Reservation] {0} {1}'.format(
                    candidate.user.first_name,
                    candidate.user.last_name
                ),
                settings.CHORAL_TRYOUTS_FROM,
                'music/ensembles/choral/email.html',
                candidate,
                [settings.MANAGERS[0][1]],
            )
            return HttpResponseRedirect(reverse_lazy('choral_tryout_success'))
    else:
        form = CandidateForm()

    return render(
        request,
        'music/ensembles/choral/form.html',
        {'form': form},
    )


@staff_member_required
def manager(request):
    """Form to allow managers to submit the form for students."""
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            cd = form.cleaned_data
            user = User.objects.get(email=cd['email'])
            candidate.user = user
            candidate.save()
            # set the time slot active state to False
            candidate.time_slot.active = False
            candidate.time_slot.save()
            return HttpResponseRedirect(reverse_lazy('choral_tryout_success'))
    else:
        form = ManagerForm()

    return render(
        request,
        'music/ensembles/choral/manager.html',
        {'form': form},
    )
