from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.core.forms import UserProfileForm
from djforms.core.models import UserProfile
from djforms.core.models import GenericChoice
from djforms.writingcurriculum.forms import ProposalForm
from djforms.writingcurriculum.models import CourseCriteria, CourseProposal

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

@login_required
def proposal_form(request, pid=None):
    copies=1
    proposal = None
    if pid:
        proposal = get_object_or_404(CourseProposal,id=pid)
        # check perms
        if proposal.user != request.user:
            raise Http404
        # create list for GET requests to populate criteria field
        criteria = []
        for copies, c in enumerate(proposal.criteria.all()):
            criteria.append({
                'id':c.id,
                'type_assignment':c.type_assignment,
                'number_pages':c.number_pages,
                'percent_grade':c.percent_grade,
                'description':c.description
            })
        # add 1 because lists are 0 based
        copies = copies+1

    if request.method=='POST':
        try:
            profile = request.user.get_profile()
        except:
            # trying to track down why a profile might not be created
            # at auth time
            logging.debug("username = %s" % request.user.username)
            profile = ''
            p = UserProfile(user=request.user)
            p.save()
            profile = request.user.get_profile()
        form = ProposalForm(request.POST, request.FILES, prefix="wac", instance=proposal)
        profile_form = UserProfileForm(request.POST, prefix="profile", instance=profile)
        pid = request.POST.getlist('wac-id[]')

        type_assignment = request.POST.getlist('wac-type_assignment[]')
        number_pages = request.POST.getlist('wac-number_pages[]')
        percent_grade = request.POST.getlist('wac-percent_grade[]')
        description = request.POST.getlist('wac-description[]')
        # len could use any of the above 4 lists
        criteria = []
        for i in range (0,len(type_assignment)):
            criteria.append({
                'id':pid[i],
                'type_assignment':type_assignment[i],
                'number_pages':number_pages[i],
                'percent_grade':percent_grade[i],
                'description':description[i]
            })
        # delete the 'doop' element used for javascript copy
        del criteria[0]

        if form.is_valid() and profile_form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.updated_by = request.user
            if request.FILES.get('wac-syllabus'):
                proposal.syllabus = request.FILES.get('wac-syllabus')
            proposal.save()
            profile_form.save()

            # CRUD
            # new list with original criteria objects
            criteria_orig = []
            for p in proposal.criteria.all():
                criteria_orig.append(p)
            # flow control vars
            x = len(criteria_orig)
            y = len(criteria)
            for i in range (0,max(x,y)):
                # if we have more exisiting criteria than new.
                # else we have more new criteria than existing.
                # update the current, delete any extras.
                if x >= y:
                    if i < y:
                        # update objects
                        criteria_orig[i].type_assignment = criteria[i]['type_assignment']
                        criteria_orig[i].number_pages = criteria[i]['number_pages']
                        criteria_orig[i].percent_grade = criteria[i]['percent_grade']
                        criteria_orig[i].description = criteria[i]['description']
                        criteria_orig[i].save()
                    else:
                        # delete any leftover objects
                        criteria_orig[i].delete()
                else:
                    if i < x:
                        # update objects
                        criteria_orig[i].type_assignment = criteria[i]['type_assignment']
                        criteria_orig[i].number_pages = criteria[i]['number_pages']
                        criteria_orig[i].percent_grade = criteria[i]['percent_grade']
                        criteria_orig[i].description = criteria[i]['description']
                        criteria_orig[i].save()
                    else:
                        c = CourseCriteria(type_assignment=criteria[i]['type_assignment'],number_pages=criteria[i]['number_pages'],percent_grade=criteria[i]['percent_grade'],description=criteria[i]['description'])
                        c.save()
                        proposal.criteria.add(c)
            # save the proposal object
            proposal.save()

            bcc = settings.MANAGERS
            recipient_list = ["msnavely@carthage.edu"]
            t = loader.get_template('writingcurriculum/proposal_email.txt')
            c = RequestContext(request, {'data':proposal,'user':request.user,'criteria':criteria})
            email = EmailMessage(("[WAC Proposal] %s: by %s %s" % (proposal.course_title,request.user.first_name,request.user.last_name)), t.render(c), request.user.email, recipient_list, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            #if proposal.syllabus:
            #    email.attach(proposal.syllabus.name.split('/')[2],proposal.syllabus)
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/writingcurriculum/success')
    else:
        if not proposal:
            criteria = [""]
            copies = len(criteria)-1
        form = ProposalForm(prefix="wac", instance=proposal)
        profile_form = UserProfileForm(prefix="profile")
    return render_to_response("writingcurriculum/proposal_form.html", {"form": form,"profile_form": profile_form, "criteria": criteria, "copies":copies}, context_instance=RequestContext(request))

@login_required
def my_proposals(request):
    objects = CourseProposal.objects.filter(user=request.user).order_by("-date_created")
    return render_to_response("writingcurriculum/my_proposals.html", {"objects": objects,}, context_instance=RequestContext(request))

