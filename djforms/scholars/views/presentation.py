# -*- coding: utf-8 -*-

import datetime
import os

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import  permission_required
from djforms.scholars.views.forms import EmailPresentersForm
from djforms.scholars.views.forms import PresentationForm
from djforms.scholars.views.forms import DEPTS
from djforms.scholars.models import Presentation
from djforms.scholars.models import Presenter
from djforms.scholars.models import PRESENTER_TYPES
from djforms.scholars.models import get_json
from djforms.core.models import Department
from djforms.core.models import YEAR_CHOICES
from djtools.utils.mail import send_mail


NOW  = datetime.datetime.now()
TODAY = datetime.date.today()
YEAR = int(NOW.year)
if int(NOW.month) > 9 and not settings.DEBUG:
    YEAR += 1

login_url = settings.LOGIN_URL

import logging
logger = logging.getLogger(__name__)


def _update_presenters(presenter, presenters):
    """Private function to update presenters."""
    presenter.first_name = presenters.first_name
    presenter.last_name = presenters.last_name
    presenter.prez_type = presenters.prez_type
    presenter.leader = presenters.leader
    presenter.college_year = presenters.college_year
    presenter.major = presenters.major
    presenter.hometown = presenters.hometown
    presenter.sponsor = presenters.sponsor
    presenter.sponsor_other = presenters.sponsor_other
    if presenters.mugshot:
        presenter.mugshot = presenters.mugshot
    if presenters.department:
        presenter.department = presenters.department
    presenter.save()
    return presenter


@login_required
def home(request):
    """Home view."""
    presentations = Presentation.objects.filter(user=request.user).filter(
        date_created__year=YEAR,
    ).order_by('title')
    return render(
        request,
        'scholars/presentation/home.html',
        {'presentations':presentations},
    )


@login_required
def form(request, pid=None):
    """Presentation form."""
    presenters = []
    presentation = None
    # flag managers
    manager = request.user.has_perm('scholars.manage_presentation')
    # get people for select field
    jason = get_json('faculty')
    faculty = []
    for jay in jason:
        faculty.append({
            'id': str(jay['id']),
            'lastname': jay['last_name'],
            'firstname': jay['first_name'],
        })
    # define our submission window
    s_date = datetime.date(
        TODAY.year,
        settings.COS_START_MONTH,
        settings.COS_START_DAY,
    )
    x_date = datetime.date(
        TODAY.year,
        settings.COS_END_MONTH,
        settings.COS_END_DAY,
    )
    expired = False
    if x_date < TODAY or s_date > TODAY:
        if not request.user.is_staff and not manager:
            expired = True

    if not pid and expired:
        # 404 after submission period has ended
        raise Http404

    if pid:
        presentation = get_object_or_404(
            Presentation,
            pk=pid,
            #date_updated__year=YEAR,
        )
        # check perms
        if presentation.user != request.user and not manager:
            return HttpResponseRedirect(reverse('auth_login'))

    # number of presenters
    copies = 0
    if presentation:
        # create list for GET requests to populate presenters fields
        for copies, prez in enumerate(presentation.presenters.all(), start=1):
            presenters.append(prez)

    if request.method=='POST':
        form=PresentationForm(request.POST,request.FILES,instance=presentation)
        first_name = request.POST.getlist('first_name[]')
        last_name = request.POST.getlist('last_name[]')
        prez_type = request.POST.getlist('prez_type[]')
        leader = request.POST.getlist('leader[]')
        college_year = request.POST.getlist('college_year[]')
        major = request.POST.getlist('major[]')
        hometown = request.POST.getlist('hometown[]')
        sponsor = request.POST.getlist('sponsor[]')
        sponsor_other = request.POST.getlist('sponsor_other[]')
        department = request.POST.getlist('department[]')
        mugshoth = request.POST.getlist('mugshoth[]')
        mugshot = request.FILES.getlist('mugshot[]')
        # leader is a boolean field and the html returns '' when
        # the checkbox is not checked
        for idx, val in enumerate(leader):
            if val == '':
                leader[idx] = False
        if pid:
            presenters = []
        # here we deal with the problem of file fields not including
        # an item in list if there is no file selected for upload.
        # mugshoth is a hidden field to mirror mugshot as counter.
        h = len(mugshot)
        for i in range (1,len(last_name)):
            if mugshoth[i] == 'True':
                try:
                    mug = mugshot[len(mugshot)-h]
                except Exception:
                    mug = None
                    logger.debug('Celebration of Scholars mugshot error.')
                h -= 1
            elif mugshoth[i]:
                mug = mugshoth[i]
            else:
                mug = None
            dept = None
            if department[i]:
                dept = Department.objects.get(name=department[i])

            presenters.append(
                Presenter(
                    first_name=first_name[i],
                    last_name=last_name[i],
                    prez_type=prez_type[i],
                    leader=leader[i],
                    college_year=college_year[i],
                    major=major[i],
                    hometown=hometown[i],
                    sponsor=sponsor[i],
                    sponsor_other=sponsor_other[i],
                    department=dept,
                    mugshot=mug,
                ),
            )

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
            for i in range (0, max(x, y)):
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
                if request.POST.get('status') == 'on':
                    presentation.status = True
                else:
                    presentation.status = False
            presentation.save()
            if not manager:
                data = {'presentation': presentation, 'pid': pid}
                status = ''
                if pid:
                    status = ' (updated)'
                subject = '''[CoS Presentation] {0}{1}: by {2} {3}'''.format(
                    presentation.title,
                    status,
                    request.user.first_name,
                    request.user.last_name,
                )
                frum = request.user.email
                send_mail (
                    request,
                    [settings.SERVER_EMAIL],
                    subject,
                    frum,
                    'scholars/presentation/email.html',
                    data,
                    reply_to=[frum,],
                    bcc=[settings.MANAGERS[0][1],],
                )
            return HttpResponseRedirect(reverse('presentation_form_done'))
        else:
            copies = len(presenters) + 1
    else:
        form = PresentationForm(instance=presentation)
        if not pid:
            copies = 1
            presenters = ['']
    context = {
        'presentation': presentation,
        'form': form,
        'presenters': presenters,
        'copies': copies,
        'faculty': faculty,
        'cyears': YEAR_CHOICES,
        'depts': DEPTS,
        'types': PRESENTER_TYPES,
        'pid': pid,
        'manager': manager,
        'expired': expired,
    }
    return render(request, 'scholars/presentation/form.html', context)


@permission_required('scholars.manage_presentation', login_url=login_url)
def manager(request):
    presentations = Presentation.objects.filter(
        date_created__year=YEAR,
    ).order_by('date_created')

    return render(
        request,
        'scholars/presentation/manager.html',
        {'presentations':presentations},
    )


@permission_required('scholars.manage_presentation', login_url=login_url)
def email_presenters(request,pid,action):
    """Send an email to the presenters and faculty sponsor."""
    form_data = None
    presentation = get_object_or_404(Presentation, pk=pid)
    if request.method=='POST':
        form = EmailPresentersForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if 'confirm' in request.POST:
                context = {'form': form, 'data': form_data, 'p': presentation}
                return render(
                    request,
                    'scholars/presenters/email_form.html',
                    context,
                )
            elif 'execute' in request.POST:
                femail = request.user.email
                to_list = [presentation.user.email]
                if presentation.leader.sponsor_email:
                    if settings.DEBUG:
                        to_list = [settings.SERVER_EMAIL,]
                        bcc = None
                    else:
                        to_list.append(presentation.leader.sponsor_email)
                        bcc = [settings.COS_EMAIL, settings.SERVER_EMAIL]
                else:
                    bcc = [request.user.email,]
                    if settings.DEBUG:
                        bcc = [settings.SERVER_EMAIL,]
                data = {'content': form_data['content']}
                sub = "[Celebration of Scholars] Info about your presentation"
                send_mail (
                    request,
                    to_list,
                    sub,
                    femail,
                    'scholars/presenters/email_data.html',
                    data,
                    reply_to=[femail,],
                    bcc=bcc,
                )
                return HttpResponseRedirect(reverse('email_presenters_done'))
            else:
                return HttpResponseRedirect(
                    reverse(
                        'email_presenters_form',
                        kwargs={'pid': pid, 'action': action},
                    ),
                )
    else:
        form = EmailPresentersForm()

    return render(
        request, 'scholars/presenters/email_form.html',
        {'form': form,'data':form_data,'p':presentation,'action':action}
    )


def archives(request, ptype, medium, year=None):
    """Year based archives, defaults to current year."""
    if year:
        year = int(year)
    else:
        year = YEAR

    template = 'scholars/{0}/archives_{1}.html'.format(ptype, medium)
    if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', template)):
        if ptype == 'presentation':
            prez = Presentation.objects.filter(
                date_updated__year=year,
            ).filter(status=True).order_by('title')
        else:
            prez = Presenter.objects.filter(
                date_updated__year=year,
            ).order_by('last_name')
        return render(request, template, {'prez': prez, 'year': year})
    else:
        raise Http404


def detail(request, pid):
    presentation = get_object_or_404(Presentation,id=pid)
    manager = request.user.has_perm('scholars.manage_presentation')
    return render(
        request, 'scholars/presentation/detail.html',
        {'p': presentation,'manager':manager}
    )


@permission_required(
    'scholars.manage_presentation', login_url=login_url)
def action(request):
    manager = request.user.has_perm('scholars.manage_presentation')
    if request.method=='POST' and manager:
        pid = int(request.POST['pid'])
        action = request.POST['action']
        presentation = get_object_or_404(Presentation,id=pid)
        if action == 'update':
            return HttpResponseRedirect(
                reverse('presentation_update', kwargs={'pid': pid})
            )
        else:
            if not action:
                action = 'update'
            return HttpResponseRedirect(
                reverse(
                    'email_presenters_form',
                    kwargs={'pid': pid, 'action': action},
                ),
            )
    else:
        raise Http404


def email_all_presenters(request):
    """Send an email to all presenters."""
    template = 'scholars/presenters/email_all_presenters.html'
    presentation = Presentation.objects.filter(date_updated__year=YEAR)
    return render(request, template, {'prez': presentation})
