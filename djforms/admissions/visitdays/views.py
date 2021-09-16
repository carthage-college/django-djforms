from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djforms.admissions.visitdays.models import VisitDay, VisitDayEvent
from djforms.admissions.visitdays.forms import *

from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

email = 'Carthage Admissions <{0}>'.format(settings.ADMISSIONS_EMAIL)
if settings.DEBUG:
    REQ_ATTR = False
else:
    REQ_ATTR = True


def visit_day_form(request, event_type):
    visit_day = get_object_or_404(VisitDay, slug=event_type)
    short = False
    if request.method=='POST':
        if visit_day.extended:
            form = VisitDayForm(
                event_type, request.POST, use_required_attribute=REQ_ATTR,
            )
        else:
            form = VisitDayBaseForm(
                event_type, request.POST, use_required_attribute=REQ_ATTR,
            )
            short = True

        if form.is_valid():
            profile = form.save()
            if visit_day.number_attend:
                event = VisitDayEvent.objects.get(pk=profile.date.id)
                event.cur_attendees = event.cur_attendees + int(profile.number_attend)
                if event.cur_attendees == event.max_attendees:
                    event.active=False
                    # send admissions email to notify them that the event is full
                    subject = "[Event FULL] {0} on {1}".format(
                        visit_day.title, profile.date,
                    )
                    send_mail(
                        request,
                        [email],
                        subject,
                        email,
                        'admissions/visitday/email_event_full.html',
                        None,
                    )
                event.save()
            # send HTML email to attendee
            if visit_day.date_alternate:
                subject = visit_day.title
            else:
                subject = "{0} on {1}".format(visit_day.title, profile.date)
            data = {'profile':profile, 'visit_day': visit_day, 'short':short}
            to_list = [profile.email]
            gmail = getattr(profile, 'guardian_email', None)
            if gmail:
                to_list.append(gmail)
            send_mail(
                request,
                to_list,
                subject,
                email,
                'admissions/visitday/email.html',
                data,
            )
            # send text mail to admissions folks
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [email]

            subject = "{0} on {1} for {2}, {3}".format(
                visit_day.title,
                profile.date,
                profile.last_name,
                profile.first_name,
            )
            send_mail(
                request,
                TO_LIST,
                subject,
                email,
                'admissions/visitday/email.txt',
                data,
            )

            return HttpResponseRedirect(
                reverse_lazy('visitday_success')
            )
    else:
        if visit_day.extended:
            form = VisitDayForm(event_type, use_required_attribute=REQ_ATTR)
        else:
            form = VisitDayBaseForm(event_type, use_required_attribute=REQ_ATTR)

    return render(
        request,
        'admissions/visitday/form.html',
        {'form': form,'event_type':event_type,'visit_day':visit_day}
    )
