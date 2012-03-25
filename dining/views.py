from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.admin.views.decorators import staff_member_required

from djforms.dining.forms import EventForm
from djforms.dining.models import Event

def event_form(request):
    if request.method=='POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.save()
            bcc = settings.MANAGERS
            recipient_list = ["larry@carthage.edu",]
            t = loader.get_template('dining/event_email.html')
            c = RequestContext(request, {'object':data,})
            email = EmailMessage(("[Event Request Form] %s: %s %s" % (data.department,data.first_name,data.last_name)), t.render(c), data.email, recipient_list, bcc, headers = {'Reply-To': data.email,'From': data.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/dining/event/success/')
    else:
        form = EventForm()
    return render_to_response("dining/event_form.html", {"form": form,}, context_instance=RequestContext(request))

@staff_member_required
def event_detail(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render_to_response("dining/event_detail.html", {"event": event,}, context_instance=RequestContext(request))

@staff_member_required
def event_archives(request):
    events = Event.objects.all().order_by("-updated_on")
    return render_to_response("dining/event_archives.html", {"events": events,}, context_instance=RequestContext(request))

