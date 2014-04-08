from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.characterquest.forms import ApplicationForm
from djforms.characterquest.forms import ApplicationProfileForm
from djforms.core.models import UserProfile

from djtools.utils.mail import send_mail

from datetime import date

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["nwinkler@carthage.edu",request.user.email]
BCC = settings.MANAGERS

@login_required
def application_profile_form(request):
    today = date.today()
    x_date = date(today.year, 4, 24)
    s_date = date(today.year, 4, 1)
    expired = False
    if x_date < today or s_date > today:
        if not request.user.is_staff and \
        not request.user.has_perm('characterquest.change_applicationprofile'):
            expired = True
    try:
        profile = request.user.get_profile()
    except:
        p = UserProfile(user=request.user)
        p.save()
        profile = request.user.get_profile()
    if request.method=='POST':
        form = ApplicationForm(request.POST, prefix="applicant")
        profile_form = ApplicationProfileForm(
            request.POST,
            prefix="profile",
            instance=profile
        )
        if form.is_valid() and profile_form.is_valid():
            profile = profile_form.save()
            applicant = form.save(commit=False)
            applicant.profile = profile
            applicant.save()

            subject = "CharacterQuest Application: %s %s" % \
                (
                    applicant.profile.user.first_name,
                    applicant.profile.user.last_name
                )
            send_mail (
                request, TO_LIST, subject, request.user.email,
                "characterquest/application_email.txt", applicant, BCC
            )

            return HttpResponseRedirect('/forms/character-quest/success/')
    else:
        form = ApplicationForm(prefix="applicant")
        profile_form=ApplicationProfileForm(prefix="profile",instance=profile)
    return render_to_response(
        "characterquest/application_form.html",
        {"form": form, "profile_form":profile_form, "expired":expired},
        context_instance=RequestContext(request)
    )
