from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from djforms.admissions.visitdays.models import VisitDay, VisitDayEvent
from djforms.admissions.visitdays.forms import *

from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

def VisitDayForm(request, event_type):
    visit_day = get_object_or_404(VisitDay, slug=event_type)
    short = False
    form_name = event_type.capitalize()+"Form"
    if request.method=='POST':
        try:
            form = str_to_class(
                "djforms.admissions.visitdays.forms", form_name
            )(event_type,request.POST)
        except:
            form = VisitDayBaseForm(event_type,request.POST)
            short = True
        if form.is_valid():
            BCC = settings.MANAGERS
            profile = form.save()
            event = VisitDayEvent.objects.get(pk=profile.date.id)
            event.cur_attendees = event.cur_attendees + profile.number_attend
            if event.cur_attendees == event.max_attendees:
                event.active=False
                # send admissions email to notify them that the event is full
                subject = "[Event FULL] {} on {}".format(
                    visit_day.title, profile.date
                )
                send_mail(
                    request, ["admissions@carthage.edu",], subject,
                    "admissions@carthage.edu",
                    "admissions/visitday/email_event_full.html", None, BCC
                )
            event.save()
            # send HTML email to attendee
            subject = "{} on {}".format(visit_day.title, profile.date)
            data = {'profile':profile,'visit_day':visit_day,'short':short}
            send_mail(
                request, [profile.email], subject, "admissions@carthage.edu",
                "admissions/visitday/email.html", data, BCC
            )
            # send text mail to admissions folks
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = ["admissions@carthage.edu"]

            subject = u"{} on {} for {}, {}".format(
                visit_day.title, profile.date, profile.last_name,
                profile.first_name
            )
            send_mail(
                request, TO_LIST, subject, "admissions@carthage.edu",
                "admissions/visitday/email.txt", data, BCC
            )

            return HttpResponseRedirect(
                reverse_lazy("visitday_success")
            )
    else:
        try:
            form = str_to_class(
                "djforms.admissions.visitdays.forms", form_name
            )(event_type)
        except:
            form = VisitDayBaseForm(event_type)
    return render_to_response(
        "admissions/visitday/form.html",
        {"form": form,"event_type":event_type,"visit_day":visit_day},
        context_instance=RequestContext(request)
    )
