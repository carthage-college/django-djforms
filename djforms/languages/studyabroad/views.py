from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djforms.languages.studyabroad.forms import StudyAbroadForm

from djtools.utils.mail import send_mail

@login_required
def study_abroad(request):
    if request.method == 'POST':
        form = StudyAbroadForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd["user"] = request.user
            email = request.user.email
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [
                    settings.STUDY_ABROAD_EMAIL, email
                ]
            subject = "Student Information for Study Abroad"
            send_mail(
                request, TO_LIST, subject, email,
                "languages/studyabroad/email.html", cd, settings.MANAGERS
            )
            return HttpResponseRedirect(
                reverse_lazy("study_abroad_success")
            )
    else:
        form = StudyAbroadForm()
    return render_to_response(
        'languages/studyabroad/form.html',
        {'form': form}, context_instance=RequestContext(request)
    )
