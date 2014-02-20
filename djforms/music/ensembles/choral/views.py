from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from djtools.utils.mail import send_mail
from djforms.music.ensembles.choral.forms import CandidateForm, ManagerForm

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
                "[Choral Tryout Reservation] %s %s" %
                (candidate.user.first_name,candidate.user.last_name),
                "dshapovalov@carthage.edu",
                "music/ensembles/choral/tryout_email.html",
                candidate, settings.MANAGERS
            )
            return HttpResponseRedirect(
                '/forms/music/ensembles/choral/tryout/success/'
            )
    else:
        form = CandidateForm()
    return render_to_response(
        "music/ensembles/choral/tryout_form.html",
        {"form": form,}, context_instance=RequestContext(request)
    )

@staff_member_required
def manager(request):
    if request.method=='POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            try:
                user = User.objects.get(username=form.cleaned_data["email"].split('@')[0])
            except:
                from random import choice
                import string
                temp_pass = ""
                for i in range(8):
                    temp_pass = temp_pass + choice(string.letters)
                user = User.objects.create_user(
                    form.cleaned_data["email"].split('@')[0],
                    form.cleaned_data["email"],
                    temp_pass
                )
            if not user.last_name:
                user.first_name=form.cleaned_data["first_name"]
                user.last_name=form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                g = Group.objects.get(name__iexact="Students")
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
    return render_to_response(
        "music/ensembles/choral/manager_form.html",
        {"form": form,}, context_instance=RequestContext(request)
    )
