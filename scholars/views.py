from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djforms.scholars.forms import PresentationForm, DEPTS
from djforms.scholars.models import Presenter, Presentation, PRESENTER_TYPES, STATUS
from djforms.core.views import send_mail
from djforms.core.models import Department, SHIRT_SIZES, YEAR_CHOICES

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["dmunk@carthage.edu",]
BCC = settings.MANAGERS

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG)

def _update_presenters(presenter, presenters):
    if presenters['department']:
        presenter.department = Department.objects.get(name=presenters['department'])
    presenter.first_name   = presenters['first_name']
    presenter.last_name    = presenters['last_name']
    presenter.prez_type    = presenters['prez_type']
    presenter.leader       = presenters['leader']
    presenter.college_year = presenters['college_year']
    presenter.major        = presenters['major']
    presenter.hometown     = presenters['hometown']
    presenter.sponsor      = presenters['sponsor']
    presenter.shirt        = presenters['shirt']
    if presenters['mugshot']:
        presenter.mugshot  = presenters['mugshot']
    presenter.save()
    return presenter

@login_required
def presentation_form(request, pid=None):
    presenters = []
    presentation = None
    manager = request.user.has_perm('scholars.manage_presentation')

    if pid:
        presentation = get_object_or_404(Presentation,id=pid)
        # check perms
        if presentation.user != request.user:
            raise Http404
        # create list for GET requests to populate criteria field
        for copies, p in enumerate(presentation.presenters.all()):
            presenters.append(p)
        # add 1 since lists are zero based
        copies += 1

    if request.method=='POST':
        form = PresentationForm(request.POST, request.FILES, instance=presentation)

        first_name   = request.POST.getlist('first_name[]')
        last_name    = request.POST.getlist('last_name[]')
        prez_type    = request.POST.getlist('prez_type[]')
        leader       = request.POST.getlist('leader[]')
        college_year = request.POST.getlist('college_year[]')
        major        = request.POST.getlist('major[]')
        hometown     = request.POST.getlist('hometown[]')
        sponsor      = request.POST.getlist('sponsor[]')
        department   = request.POST.getlist('department[]')
        shirt        = request.POST.getlist('shirt[]')
        mugshoth     = request.POST.getlist('mugshoth[]')
        mugshot      = request.FILES.getlist('mugshot[]')

        if pid:
            presenters = []
        # here we deal with the problem of file fields not including
        # an item in list if there is no file selected for upload.
        # mugshoth is a hidden field to mirror mugshot as counter.
        h = len(mugshot)
        for i in range (1,len(last_name)):
            if mugshoth[i] == "True":
                mug = mugshot[len(mugshot)-h]
                h -= 1
            else:
                mug = None

            presenters.append({
                'first_name':first_name[i],'last_name':last_name[i],
                'prez_type':prez_type[i], 'leader':leader[i],
                'college_year':college_year[i], 'major':major[i],
                'hometown':hometown[i], 'sponsor':sponsor[i],
                'department':department[i], 'shirt':shirt[i],
                'mugshot':mug
            })

        if form.is_valid():
            # save and include some other values and commit
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.updated_by = request.user
            if request.FILES.get('abstract_file'):
                presentation.abstract_file = request.FILES.get('abstract_file')
            if request.POST.get('status'):
                presentation.status = request.POST.get('status')
            presentation.save()

            # CRUD
            # new list with original presenter objects
            presenters_orig = []
            for p in presentation.presenters.all():
                presenters_orig.append(p)
            # flow control vars
            x = len(presenters_orig)
            y = len(presenters)
            for i in range (0,max(x,y)):
                # if we have more exisiting presenters than new.
                # else we have more new presenters than existing.
                # update the current, delete any extras.
                if x >= y:
                    if i < y:
                        # update objects
                        p = _update_presenters(presenters_orig[i], presenters[i])
                    else:
                        # delete any leftover objects
                        presenters_orig[i].delete()
                else:
                    if i < x:
                        # update objects
                        p = _update_presenters(presenters_orig[i], presenters[i])
                    else:
                        presenter = Presenter()
                        p = _update_presenters(presenter, presenters[i])
                        presentation.presenters.add(p)
                if p.leader:
                    presentation.leader = p
            # save the presentation object
            presentation.save()
            data = {"presentation":presentation,"pid":pid,}
            status = ""
            if pid:
                status = " (updated)"
            subject = "[Celebration of Scholars Presentation] %s%s: by %s %s" % (presentation.title,status,request.user.first_name,request.user.last_name)
            send_mail(request, TO_LIST, subject, request.user.email, "scholars/presentation_email.html", data, BCC)
            return HttpResponseRedirect('/forms/scholars/presentation/success/')
        else:
            copies = len(presenters) + 1

    else:
        form = PresentationForm(instance=presentation)
        if not pid:
            presenters = [""]
            copies = 1

    context = {"form":form,"presenters":presenters,"copies":copies,"shirts":SHIRT_SIZES,"cyears":YEAR_CHOICES,"depts":DEPTS,"types":PRESENTER_TYPES,"pid":pid,"manager":manager,"status":STATUS,}
    return render_to_response("scholars/presentation_form.html", context, context_instance=RequestContext(request))


def scholars_archives(request, year=None):
    if year:
        year = int(year)
    else:
        year = int(datetime.date.today().year)
    presentations = Presentation.objects.filter(date_created__year=year).order_by("user__last_name")
    return render_to_response("scholars/presentation_archives.html", {"presentations": presentations,"year":year,}, context_instance=RequestContext(request))

def presentation_detail(request):
    return render_to_response("scholars/presentation_detail.html", {"presentation": presentation,}, context_instance=RequestContext(request))

