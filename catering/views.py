from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader

from djforms.catering.forms import EventForm1, EventForm2, EventForm3, EventForm4, EventForm5
from djforms.catering.models import Event

import os.path

storage_location = os.path.join(settings.MEDIA_ROOT, "files/catering/temp/")
storage = FileSystemStorage(location=storage_location)

class CateringEventWizard(SessionWizardView):
    """
    Form wizard view for processing the event steps
    """
    file_storage = storage
    template_name = "catering/event_form_wizard.html"

    def done(self, form_list, **kwargs):
        event = Event()
        xfields = {'open_to':"", 'room_set_up':"", 'beverages':""}
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                if field not in xfields:
                    setattr(event, field, value)
                else:
                    xfields[field] = value
        event.user = self.request.user
        event.save()
        event.open_to = xfields['open_to']
        event.room_set_up = xfields['room_set_up']
        event.beverages = xfields['beverages']
        event.save()
        bcc = settings.MANAGERS
        recipient_list = ["dhoffman1@carthage.edu","jchilson@carthage.edu,","mmichaud@carthage.edu", "jklabechek@carthage.edu"]
        t = loader.get_template('catering/event_email.html')
        c = RequestContext(self.request, {'event':event,})
        email = event.user.email
        recipient_list.append(email)
        email = EmailMessage(("[Event Request Form] %s: %s %s" % (event.department,event.user.first_name,event.user.last_name)), t.render(c), email, recipient_list, bcc, headers = {'Reply-To': email,'From': email})
        email.content_subtype = "html"
        email.send(fail_silently=True)
        return HttpResponseRedirect('http://%s/forms/catering/event/success/' % settings.SERVER_URL)

    def get_form(self, step=None, data=None, files=None):
        form = super(CateringEventWizard, self).get_form(step, data, files)
        #template_name = "catering/event_form_%s.html" % step
        #template_name = "catering/event_form_wizard.html"
        return form

@staff_member_required
def event_detail(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render_to_response("catering/event_detail.html", {"event": event,}, context_instance=RequestContext(request))

@staff_member_required
def event_archives(request):
    events = Event.objects.all().order_by("-updated_on")
    return render_to_response("catering/event_archives.html", {"events": events,}, context_instance=RequestContext(request))

