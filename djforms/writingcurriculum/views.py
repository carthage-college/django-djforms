# -*- coding: utf-8 -*-

"""Views for all requests."""

import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from djforms.core.forms import UserProfileForm
from djforms.core.models import UserProfile
from djforms.writingcurriculum.forms import ProposalForm
from djforms.writingcurriculum.models import CourseCriteria
from djforms.writingcurriculum.models import CourseProposal
from djtools.utils.mail import send_mail


@login_required
def proposal_form(request, pid=None):
    if settings.DEBUG:
        to_list = [settings.SERVER_EMAIL]
    else:
        to_list = settings.WAC_EMAIL_LIST

    copies=1
    proposal = None
    if pid:
        proposal = get_object_or_404(CourseProposal, pk=pid)
        # check perms
        if proposal.user != request.user and not request.user.is_superuser:
            raise Http404
        # create list for GET requests to populate criteria field
        criteria = []
        for copies, c in enumerate(proposal.criteria.all()):
            criteria.append({
                'id': c.id,
                'type_assignment': c.type_assignment,
                'number_pages': c.number_pages,
                'percent_grade': c.percent_grade,
                'description': c.description,
            })
        # add 1 because lists are 0 based
        copies += 1

    if request.method == 'POST':
        try:
            profile = request.user.userprofile
        except Exception:
            p = UserProfile(user=request.user)
            p.save()
            profile = request.user.userprofile
        form = ProposalForm(
            request.POST, request.FILES, prefix='wac', instance=proposal,
        )
        profile_form = UserProfileForm(
            request.POST, prefix='profile', instance=profile,
        )
        pids = request.POST.getlist('wac-id[]')

        type_assignment = request.POST.getlist('wac-type_assignment[]')
        number_pages = request.POST.getlist('wac-number_pages[]')
        percent_grade = request.POST.getlist('wac-percent_grade[]')
        description = request.POST.getlist('wac-description[]')
        # len could use any of the above 4 lists
        criteria = []
        for i in range (0,len(type_assignment)):
            criteria.append({
                'id': pids[i],
                'type_assignment': type_assignment[i],
                'number_pages': number_pages[i],
                'percent_grade': percent_grade[i],
                'description': description[i],
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
            for i in range (0, max(x, y)):
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
                        c = CourseCriteria(
                            type_assignment=criteria[i]['type_assignment'],
                            number_pages=criteria[i]['number_pages'],
                            percent_grade=criteria[i]['percent_grade'],
                            description=criteria[i]['description'],
                        )
                        c.save()
                        proposal.criteria.add(c)
            # save the proposal object
            proposal.save()
            subject ="[WAC Proposal] {0}: by {1} {2}".format(
                proposal.course_title,
                request.user.first_name,
                request.user.last_name,
            )
            to_list.append(request.user.email)
            send_mail(
                request,
                to_list,
                subject,
                request.user.email,
                'writingcurriculum/email.html',
                {'proposal': proposal, 'user': request.user, 'criteria': criteria},
                [settings.SERVER_EMAIL],
            )
            return HttpResponseRedirect(reverse_lazy('proposal_success'))
    else:
        if not proposal:
            criteria = ['']
            copies = len(criteria)
        form = ProposalForm(prefix='wac', instance=proposal)
        profile_form = UserProfileForm(prefix='profile')

    # academic year
    today = datetime.date.today()
    year = today.year + 1
    year_past = year - 1
    if today.month > 3:
        year_past = year
        year += 1

    return render(
        request,
        'writingcurriculum/form.html',
        {
            'form': form,
            'profile_form': profile_form,
            'criteria': criteria,
            'copies': copies,
            'year': year,
            'year_past': year_past,
        },
    )


@login_required
def my_proposals(request):
    objects = CourseProposal.objects.filter(
        user=request.user,
    ).order_by('-date_created')

    return render(
        request,
        'writingcurriculum/my_proposals.html',
        {'objects': objects},
    )
