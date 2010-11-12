from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.admissions.visitdays.models import VisitDay
from djforms.admissions.visitdays.forms import VisitDayBaseForm, WeekdayForm, SaturdayForm, TransferForm

def VisitDayForm(request, event_type):
    visit_day = get_object_or_404(VisitDay, slug=event_type)
    if request.method=='POST':
        try:
            form = eval(event_type.capitalize()+"Form")(event_type,request.POST)
        except:
            form = VisitDayBaseForm(event_type,request.POST)
        if form.is_valid():
            profile = form.save()
            bcc = settings.MANAGERS
            to = ["larry@carthage.edu",profile.email]
            t = loader.get_template('characterquest/application_email.txt')
            c = RequestContext(request, {'data':applicant,})
            email = EmailMessage(("Visit Day Registration Form: %s on %s" % (event_type.capitalize,profile.date)), t.render(c), profile.email, to, bcc, headers = {'Reply-To': profile.email,'From': profile.email})
            email.content_subtype = "html"
            #email.attach_file('/d2/django_projects/')
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/admissions/success')
    else:
        try:
            form = eval(event_type.capitalize()+"Form")(event_type)
        except:
            form = VisitDayBaseForm(event_type)
    return render_to_response("admissions/visitday_form.html", {"form": form,"event_type":event_type,"visit_day":visit_day}, context_instance=RequestContext(request))