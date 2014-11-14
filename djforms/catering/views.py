from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.admin.views.decorators import staff_member_required

from djforms.catering.forms import EventForm1, EventForm2, EventForm3
from djforms.catering.forms import EventForm4, EventForm5
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
        if settings.DEBUG:
            TO_LIST = [settings.SERVER_EMAIL]
        else:
            TO_LIST = [
                "dhoffman1@carthage.edu","svanags@carthage.edu",
                "mmichaud@carthage.edu", "jklabechek@carthage.edu"
            ]

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
        t = loader.get_template('catering/event_email.html')
        c = RequestContext(self.request, {'event':event,})
        email = event.user.email
        TO_LIST.append(email)
        email = EmailMessage(
            ("[Event Request Form] %s: %s %s" %
                (
                    event.department,event.user.first_name,event.user.last_name
                )
            ), t.render(c), email, TO_LIST, settings.MANAGERS,
            headers = {'Reply-To': email,'From': email}
        )
        email.content_subtype = "html"
        email.send(fail_silently=True)
        return HttpResponseRedirect(
            reverse_lazy("catering_event_success")
        )

    def get_form(self, step=None, data=None, files=None):
        form = super(CateringEventWizard, self).get_form(step, data, files)
        #template_name = "catering/event_form_%s.html" % step
        #template_name = "catering/event_form_wizard.html"
        return form

@staff_member_required
def event_detail(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render_to_response(
        "catering/event_detail.html",
        {"event": event,},
        context_instance=RequestContext(request)
    )

@staff_member_required
def event_archives(request):
    events = Event.objects.all().order_by("-updated_on")
    return render_to_response(
        "catering/event_archives.html",
        {"events": events,},
        context_instance=RequestContext(request)
    )
