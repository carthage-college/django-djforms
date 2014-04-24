from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from djforms.scholars.views.forms import EmailPresentersForm, PresentationForm
from djforms.scholars.views.forms import DEPTS
from djforms.scholars.models import Presenter, Presentation, PRESENTER_TYPES
from djforms.scholars.models import get_json
from djforms.core.models import Department, YEAR_CHOICES

from djtools.utils.mail import send_mail

import datetime, os

NOW  = datetime.datetime.now()
YEAR = int(NOW.year)
if int(NOW.month) > 9 and not settings.DEBUG:
    YEAR += 1

TO_LIST = ["larry@carthage.edu",]
BCC = settings.MANAGERS

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG)

def _update_presenters(presenter, presenters):
    presenter.first_name   = presenters.first_name
    presenter.last_name    = presenters.last_name
    presenter.prez_type    = presenters.prez_type
    presenter.leader       = presenters.leader
    presenter.college_year = presenters.college_year
    presenter.major        = presenters.major
    presenter.hometown     = presenters.hometown
    presenter.sponsor      = presenters.sponsor
    presenter.sponsor_other= presenters.sponsor_other
    if presenters.mugshot:
        presenter.mugshot  = presenters.mugshot
    if presenters.department:
        presenter.department  = presenters.department
    presenter.save()
    return presenter

@login_required
def form(request, pid=None):
    presenters = []
    presentation = None
    manager = request.user.has_perm('scholars.manage_presentation')
    # get people for select field
    jason  = get_json("faculty")
    faculty = settings.COS_FACULTY
    for j in jason:
        faculty.append(j[j.keys()[0]])

    if pid:
        presentation = get_object_or_404(
            Presentation,id=pid,date_updated__year=YEAR
        )
        # check perms
        if presentation.user != request.user and not manager:
            raise Http404
    else:
        try:
            presentation = Presentation.objects.get(
                user=request.user,date_updated__year=YEAR
            )
            pid = presentation.id
        except:
            pass
            # 404 after submission period has ended
            #raise Http404

    if presentation:
        # create list for GET requests to populate presenters fields
        for copies, p in enumerate(presentation.presenters.all()):
            presenters.append(p)
        # add 1 since lists are zero based
        copies += 1


    if request.method=='POST':
        form=PresentationForm(request.POST,request.FILES,instance=presentation)

        first_name   = request.POST.getlist('first_name[]')
        last_name    = request.POST.getlist('last_name[]')
        prez_type    = request.POST.getlist('prez_type[]')
        leader       = request.POST.getlist('leader[]')
        college_year = request.POST.getlist('college_year[]')
        major        = request.POST.getlist('major[]')
        hometown     = request.POST.getlist('hometown[]')
        sponsor      = request.POST.getlist('sponsor[]')
        sponsor_other= request.POST.getlist('sponsor_other[]')
        department   = request.POST.getlist('department[]')
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
                try:
                    mug = mugshot[len(mugshot)-h]
                except:
                    mug = None
                    logging.exception("Celebration of Scholars mugshot error.")
                h -= 1
            elif mugshoth[i]:
                mug = mugshoth[i]
            else:
                mug = None
            dept = None
            if department[i]:
                dept = Department.objects.get(name=department[i])

            presenters.append(Presenter(
                first_name=first_name[i],last_name=last_name[i],
                prez_type=prez_type[i],leader=leader[i],
                college_year=college_year[i],major=major[i],
                hometown=hometown[i],sponsor=sponsor[i],
                sponsor_other=sponsor_other[i],department=dept,mugshot=mug))

        if form.is_valid():
            if presentation:
                user = presentation.user
            else:
                user = request.user
            # save and include some other values and commit
            presentation = form.save(commit=False)
            presentation.user = user
            presentation.updated_by = request.user
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
            if manager:
                if request.POST.get('status') == "on":
                    presentation.status = True
                else:
                    presentation.status = False
            presentation.save()
            if not manager:
                data = {"presentation":presentation,"pid":pid,}
                status = ""
                if pid:
                    status = " (updated)"
                subject = """[CoS Presentation] %s%s: by %s %s""" % (
                    presentation.title,status,request.user.first_name,
                    request.user.last_name
                )
                send_mail (
                    request, TO_LIST, subject, request.user.email,
                    "scholars/presentation/email.html", data, BCC
                )
            return HttpResponseRedirect(reverse("presentation_form_done"))
        else:
            copies = len(presenters) + 1

    else:
        form = PresentationForm(instance=presentation)
        if not pid:
            presenters = [""]
            copies = 1

    context = {
        "presentation":presentation,"form":form,
        "presenters":presenters,"copies":copies,
        "faculty":faculty,"cyears":YEAR_CHOICES,
        "depts":DEPTS,"types":PRESENTER_TYPES,
        "pid":pid,"manager":manager
    }
    return render_to_response (
        "scholars/presentation/form.html",
        context, context_instance=RequestContext(request)
    )


@permission_required(
    'scholars.manage_presentation',
    login_url="/forms/accounts/login/"
)
def manager(request):
    p = Presentation.objects.filter(date_updated__year=YEAR)
    presentations = p.order_by("-date_created")
    #presentations = Presentation.objects.all().order_by("-date_created")
    return render_to_response (
        "scholars/presentation/manager.html",
        {"presentations":presentations,},
        context_instance=RequestContext(request)
    )


@permission_required(
    'scholars.manage_presentation',
    login_url="/forms/accounts/login/"
)
def email_presenters(request,pid,action):
    """
    method to send an email to the presenters and faculty sponsor
    """
    form_data = None
    presentation = get_object_or_404(Presentation,id=pid)
    if request.method=='POST':
        form = EmailPresentersForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if "confirm" in request.POST:
                context = {"form":form,"data":form_data,"p":presentation}
                return render_to_response (
                    "scholars/presenters/email_form.html",
                    context,context_instance=RequestContext(request))
            elif "execute" in request.POST:
                FEMAIL = request.user.email
                BCC = ( ('larry@carthage.edu'), )
                TO_LIST = [presentation.user.email,]
                if presentation.leader.sponsor_email:
                    if settings.DEBUG:
                        TO_LIST.append("bridge@carthage.edu")
                    else:
                        TO_LIST.append(presentation.leader.sponsor_email)
                data = {"content":form_data["content"]}
                sub = "[Celebration of Scholars] Info about your presentation",
                send_mail (
                    request, TO_LIST, sub,
                    FEMAIL, "scholars/presenters/email_data.html", data, BCC
                )
                return HttpResponseRedirect(reverse("email_presenters_done"))
            else:
                return HttpResponseRedirect(reverse("email_presenters_form"))
    else:
        form = EmailPresentersForm()

    return render_to_response (
        "scholars/presenters/email_form.html",
        {"form": form,"data":form_data,"p":presentation,"action":action},
        context_instance=RequestContext(request)
    )


def archives(request, ptype, medium, year=None):
    """
    Year based archives, defaults to current year
    """
    if year:
        year = int(year)
    else:
        year = YEAR

    template = "scholars/%s/archives_%s.html" % (ptype, medium)

    if os.path.isfile(os.path.join(settings.ROOT_DIR, "templates", template)):
        if ptype == "presentation":
            p = Presentation.objects.filter(date_updated__year=year)
            p.filter(status=True).order_by("user__last_name")
        else:
            prez = Presenter.objects.filter(date_updated__year=year)
            p = prez.order_by("last_name")

        return render_to_response (
            template, {"prez": p,"year":year,},
            context_instance=RequestContext(request)
        )
    else:
        raise Http404, "Page not found"


def detail(request, pid):
    presentation = get_object_or_404(Presentation,id=pid)
    manager = request.user.has_perm('scholars.manage_presentation')
    return render_to_response (
        "scholars/presentation/detail.html",
        {"p": presentation,"manager":manager},
        context_instance=RequestContext(request)
    )


@permission_required('scholars.manage_presentation', login_url="/forms/accounts/login/")
def action(request):
    manager = request.user.has_perm('scholars.manage_presentation')
    if request.method=='POST' and manager:
        pid = int(request.POST["pid"])
        action = request.POST["action"]
        presentation = get_object_or_404(Presentation,id=pid)
        if action == "update":
            return HttpResponseRedirect(reverse('presentation_update', args=[pid]))
        else:
            return HttpResponseRedirect(reverse('email_presenters', args=[pid,action]))
    else:
        raise Http404, "Page not found"

def email_all_presenters(request):
    """
    Send an email to all presenters
    """
    template = "scholars/presenters/email_all_presenters.html"

    p = Presentation.objects.filter(date_updated__year=year)

    return render_to_response (
        template, {"prez": p,},
        context_instance=RequestContext(request)
    )
