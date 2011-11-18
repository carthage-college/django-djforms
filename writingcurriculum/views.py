from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.core.forms import UserProfileForm
from djforms.core.models import UserProfile
from djforms.core.models import GenericChoice
from djforms.writingcurriculum.forms import ProposalForm
from djforms.writingcurriculum.models import CourseCriteria, CourseProposal, Criterion

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

@login_required
def proposal_form(request, pid=None):
    criteria = {}
    proposal = None
    if pid:
        proposal = get_object_or_404(CourseProposal,id=pid)
        #criteria = proposal.criteria.all()
        x = 1
        for c in proposal.coursecriteria_set.all():
            criteria[x] = {
                'id':c.id,
                'type_assignment':c.type_assignment,
                'number_pages':c.number_pages,
                'percent_grade':c.percent_grade,
                'description':c.description,
            }
            x += 1
        #copies = criteria.count
        copies = x-1

    if request.method=='POST':
        try:
            profile = request.user.get_profile()
        except:
            # trying to track down why a profile might not be created
            # at auth time
            logging.debug("username = %s" % request.user.username)
            profile = ''
            #p = UserProfile(user=request.user)
            #p.save()
            #profile = request.user.get_profile()
        form = ProposalForm(request.POST, request.FILES, prefix="wac", instance=proposal)
        profile_form = UserProfileForm(request.POST, prefix="profile", instance=profile)
        pid = request.POST.getlist('wac-id[]')
        type_assignment = request.POST.getlist('wac-type_assignment[]')
        number_pages = request.POST.getlist('wac-number_pages[]')
        percent_grade = request.POST.getlist('wac-percent_grade[]')
        description = request.POST.getlist('wac-description[]')
        for x in range (1,len(type_assignment)):
            criteria[x] = {
                'id':pid[x],
                'type_assignment':type_assignment[x],
                'number_pages':number_pages[x],
                'percent_grade':percent_grade[x],
                'description':description[x],
            }
        if form.is_valid() and profile_form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.updated_by = request.user
            proposal.syllabus = request.FILES.get('wac-syllabus')
            proposal.save()
            profile_form.save()
            for key in criteria:
                criterion = Criterion("%s %s" %(c.course_title, key)).save()
                c = CourseCriteria(criterion, proposal.id, criteria[key]['type_assignment'],criteria[key]['number_pages'],criteria[key]['percent_grade'],criteria[key]['description'])
                c.save()
            proposal.save()

            bcc = settings.MANAGERS
            #recipient_list = ["msnavely@carthage.edu"]
            recipient_list = ["larry@carthage.edu"]
            t = loader.get_template('writingcurriculum/proposal_email.txt')
            c = RequestContext(request, {'data':proposal,'user':request.user,'criteria':criteria})
            email = EmailMessage(("[WAC Proposal] %s: by %s %s" % (proposal.course_title,request.user.first_name,request.user.last_name)), t.render(c), request.user.email, recipient_list, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/writingcurriculum/success')
    else:
        if not proposal:
            criteria[0] = ""
            copies = len(criteria)-1
        form = ProposalForm(prefix="wac", instance=proposal)
        profile_form = UserProfileForm(prefix="profile")
    return render_to_response("writingcurriculum/proposal_form.html", {"form": form,"profile_form": profile_form, "criteria": criteria, "copies":copies}, context_instance=RequestContext(request))

@login_required
def my_proposals(request):
    objects = CourseProposal.objects.all().order_by("-date_created")
    return render_to_response("writingcurriculum/my_proposals.html", {"objects": objects,}, context_instance=RequestContext(request))

