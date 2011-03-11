from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from djforms.core.forms import UserProfileForm
from djforms.core.models import UserProfile
from djforms.core.models import GenericChoice
from djforms.writingcurriculum.forms import SubmissionForm
from djforms.writingcurriculum.models import Criterion, CourseCriteria

@login_required
def submission_form(request):
    criteria = {}
    if request.method=='POST':
        try:
            profile = request.user.get_profile()
        except:
            p = UserProfile(user=request.user)
            p.save()
            profile = request.user.get_profile()
        form = SubmissionForm(request.POST, request.FILES, prefix="wac")
        profile_form = UserProfileForm(request.POST, prefix="profile", instance=profile)
        type_assignment = request.POST.getlist('wac-type_assignment[]')
        number_pages = request.POST.getlist('wac-number_pages[]')
        percent_grade = request.POST.getlist('wac-percent_grade[]')
        description = request.POST.getlist('wac-description[]')
        for x in range (1,len(type_assignment)):
            criteria[x] = {
                'type_assignment':type_assignment[x],
                'number_pages':number_pages[x],
                'percent_grade':percent_grade[x],
                'description':description[x],
            }
        if form.is_valid() and profile_form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.updated_by = request.user
            submission.syllabus = request.FILES.get('wac-syllabus')
            submission.save()
            profile_form.save()
            for key in criteria:
                c = CourseCriteria(None, None, submission.id, criteria[key]['type_assignment'],criteria[key]['number_pages'],criteria[key]['percent_grade'],criteria[key]['description'])
                c.save()
                #submission.criteria.add(c)
            submission.save()

            bcc = settings.MANAGERS
            recipient_list = ["msnavely@carthage.edu"]
            t = loader.get_template('writingcurriculum/submission_email.txt')
            c = RequestContext(request, {'data':submission,'user':request.user,'criteria':criteria})
            email = EmailMessage(("[WAC Submission] %s: by %s %s" % (submission.course_title,request.user.first_name,request.user.last_name)), t.render(c), request.user.email, recipient_list, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/writingcurriculum/success')
    else:
        criteria[0] = ""
        form = SubmissionForm(prefix="wac")
        profile_form = UserProfileForm(prefix="profile")
    return render_to_response("writingcurriculum/submission_form.html", {"form": form,"profile_form": profile_form, "criteria": criteria, "copies":len(criteria)-1}, context_instance=RequestContext(request))
