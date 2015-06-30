from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.admissions.visitdays.models import VisitDay, VisitDayEvent
from djforms.admissions.visitdays.forms import *

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
            bcc = settings.MANAGERS
            profile = form.save()
            event = VisitDayEvent.objects.get(pk=profile.date.id)
            event.cur_attendees = event.cur_attendees + profile.number_attend
            if event.cur_attendees == event.max_attendees:
                event.active=False
                # send admissions email to notify them that the event is full
                email = EmailMessage(
                    ("[Event FULL] %s on %s" % (visit_day.title,profile.date)),
                    "event is full.", "admissions@carthage.edu",u
                    ["admissions@carthage.edu"], bcc
                )
                email.send(fail_silently=True)
            event.save()
            # send HTML email to attendee
            to = [profile.email]
            #to = ["larry@carthage.edu"]
            t = loader.get_template('admissions/visitday/email.html')
            c = RequestContext(
                request, {'data':profile,'visit_day':visit_day,'short':short}
            )
            email = EmailMessage(
                ("%s on %s" % (visit_day.title,profile.date)),
                t.render(c), "admissions@carthage.edu", to, bcc
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            # send text mail to admissions folks
            to = ["admissions@carthage.edu"]
            #to = ["larry@carthage.edu"]
            t = loader.get_template('admissions/visitday/email.txt')
            c = RequestContext(
                request, {'data':profile,'visit_day':visit_day,'short':short}
            )
            email = EmailMessage(
                ("%s on %s for %s, %s" % (
                    visit_day.title,profile.date,profile.last_name,
                    profile.first_name)
                ),
                t.render(c), 'admissions@carthage.edu', to, bcc,
                headers = {'Reply-To': profile.email,}
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)

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
