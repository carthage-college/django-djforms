from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.scholars.forms import PresentationForm
from djforms.scholars.models import Presenter, Presentation
from djforms.core.views import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["dmunk@carthage.edu",]
BCC = settings.MANAGERS

def _update_presenters(presenter, presenters):
    presenter.first_name   = presenters['first_name']
    presenter.last_name    = presenters['last_name']
    presenter.prez_type    = presenters['prez_type']
    presenter.college_year = presenters['college_year']
    presenter.major        = presenters['major']
    presenter.hometown     = presenters['hometown']
    presenter.sponsor      = presenters['sponsor']
    presenter.department   = presenters['department']
    presenter.shirt        = presenters['shirt']
    presenter.mugshot      = presenters['mugshot']
    presenter.save()
    return presenter

@login_required
def presentation_form(request, pid=None):
    copies=1
    presentation = None
    if pid:
        presentation = get_object_or_404(Presentation,id=pid)
        # check perms
        if presentation.user != request.user:
            raise Http404
        # create list for GET requests to populate criteria field
        presenters = []
        for copies, p in enumerate(presentation.presenters.all()):
            if not p.leader:
                presenters.append(p)
        # add 1 because lists are 0 based
        copies = copies+1

    if request.method=='POST':
        form = PresentationlForm(request.POST, request.FILES, instance=presentation)
        pids = request.POST.getlist('pid[]')

        first_name   = request.POST.getlist('prez-first_name[]')
        last_name    = request.POST.getlist('prez-last_name[]')
        prez_type    = request.POST.getlist('prez-prez_type[]')
        college_year = request.POST.getlist('prez-college_year[]')
        major        = request.POST.getlist('prez-major[]')
        hometown     = request.POST.getlist('prez-hometown[]')
        sponsor      = request.POST.getlist('prez-sponsor[]')
        department   = request.POST.getlist('prez-department[]')
        shirt        = request.POST.getlist('prez-shirt[]')
        mugshot      = request.POST.getlist('prez-mugshot[]')

        presenters = []
        # len could use any of the above
        for i in range (0,len(last_name)):
            presenters.append({
                'id':pids[i],
                'first_name':first_name[i],
                'last_name':last_name[i],
                'prez_type':prez_type[i],
                'college_year':college_year[i],
                'major':major[i],
                'hometown':hometown[i],
                'sponsor':sponsor[i],
                'department':department[i],
                'shirt':shirt[i],
                'mugshot':mugshot[i]
            })
        # delete the 'doop' element used for javascript copy
        del presenters[0]

        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.leader = request.user
            presentation.updated_by = request.user
            if request.FILES.get('abstract_file'):
                presentation.abstract_file = request.FILES.get('abstract_file')
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
                # if we have more exisiting criteria than new.
                # else we have more new criteria than existing.
                # update the current, delete any extras.
                if x >= y:
                    if i < y:
                        # update objects
                        _update_presenters(presenters_orig[i], presenters[i])
                    else:
                        # delete any leftover objects
                        presenters_orig[i].delete()
                else:
                    if i < x:
                        # update objects
                        _update_presenters(presenters_orig[i], presenters[i])
                    else:
                        presenter = Presenter()
                        p = _update_presenters(presenter, presenters[i])
                        presentation.presenters.add(p)
            # save the presentation object
            presentation.save()
            subject = "[Celebration of Scholars Presentation] %s: by %s %s" % (presentation.title,request.user.first_name,request.user.last_name)
            send_mail(request, TO_LIST, subject, request.user.email, "scholars/presentation_email.html", presentation, BCC)
            return HttpResponseRedirect('/forms/scholars/success/')
    else:
        if not presentation:
            presenters = [""]
            copies = len(presenters)-1
        form = PresentationForm(instance=presentation)
    return render_to_response("scholars/presentation_form.html", {"form": form, "presenters": presenters, "copies":copies}, context_instance=RequestContext(request))

def presentation_archives(request, year=None):
    if year:
        year = int(year)
    else:
        year = int(datetime.date.today().year)
    presentations = Presentation.objects.filter(date_created__year=year).order_by("user__last_name")
    return render_to_response("scholars/presentation_archives.html", {"presentations": presentations,"year":year,}, context_instance=RequestContext(request))

def presentation_detail(request):
    return render_to_response("scholars/presentation_detail.html", {"presentation": presentation,}, context_instance=RequestContext(request))

