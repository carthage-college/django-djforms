from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from djforms.music.ensembles.choral.forms import CandidateForm, ManagerForm

from djtools.utils.mail import send_mail

import datetime


@login_required
def candidate(request):
    if request.method=='POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            # set the time slot active state to False
            candidate.time_slot.active = False
            candidate.time_slot.save()
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL,]
            else:
                TO_LIST = [candidate.user.email,]
            send_mail(
                request, TO_LIST,
                u"[Choral Tryout Reservation] {} {}".format(
                    candidate.user.first_name,candidate.user.last_name
                ), settings.CHORAL_TRYOUTS_FROM,
                'music/ensembles/choral/email.html',
                candidate, [settings.MANAGERS[0][1], settings.CHORAL_TRYOUTS_FROM]
            )
            return HttpResponseRedirect(
                reverse_lazy('choral_tryout_success')
            )
    else:
        form = CandidateForm()

    return render(
        request, 'music/ensembles/choral/form.html',
        {'form': form,}
    )


@staff_member_required
def manager(request):
    if request.method=='POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            try:
                user = User.objects.get(
                    username=form.cleaned_data['email'].split('@')[0]
                )
            except:
                from random import choice
                import string
                temp_pass = ''
                for i in range(8):
                    temp_pass = temp_pass + choice(string.letters)
                user = User.objects.create_user(
                    form.cleaned_data['email'].split('@')[0],
                    form.cleaned_data['email'],
                    temp_pass
                )
            if not user.last_name:
                user.first_name=form.cleaned_data['first_name']
                user.last_name=form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                g = Group.objects.get(name__iexact='carthageStudentStatus')
                g.user_set.add(user)
            candidate.user = user
            candidate.save()
            # set the time slot active state to False
            candidate.time_slot.active = False
            candidate.time_slot.save()
            return HttpResponseRedirect(
                '/forms/music/ensembles/choral/tryout/success/'
            )
    else:
        form = ManagerForm()

    return render(
        request,
        'music/ensembles/choral/manager.html',
        {'form': form,}
    )
