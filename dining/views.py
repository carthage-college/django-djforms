from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader

from djforms.dining.forms import EventForm1, EventForm2, EventForm3, EventForm4, EventForm5
from djforms.dining.models import Event

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG,)

class CateringEventWizard(SessionWizardView):
    """
    Form wizard view for processing the event steps
    """
    file_storage = FileSystemStorage(location='/assets/files/dining')
    template_name = "dining/event_form_wizard.html"

    def done(self, form_list, **kwargs):
        #logging.debug("request = %s" % self.request)
        """
        event = Event()
        event.save()
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                setattr(event, field, value)
        event.save()
        logging.debug("event = %s" % event.__dict__)
        """
        """
        bcc = settings.MANAGERS
        recipient_list = ["larry@carthage.edu",]
        t = loader.get_template('dining/event_email.html')
        c = RequestContext(request, {'object':"boo!",})
        #email = EmailMessage(("[Event Request Form] %s: %s %s" % (data.department,data.first_name,data.last_name)), t.render(c), data.email, recipient_list, bcc, headers = {'Reply-To': data.email,'From': data.email})
        e = "plungerman@gmail.com"
        email = EmailMessage("[Event Request Form] test", t.render(c), e, recipient_list, bcc, headers = {'Reply-To': e,'From': e})
        email.content_subtype = "html"
        email.send(fail_silently=True)
        """
        return HttpResponseRedirect('/forms/dining/event/success/')

    def get_form(self, step=None, data=None, files=None):
        form = super(CateringEventWizard, self).get_form(step, data, files)
        if step == '1':
            form.user = self.request.user
        #template_name = "dining/event_form_%s.html" % step
        #template_name = "dining/event_form_wizard.html"
        return form

    """
    def get_form_instance(self, step):
        return self.instance_dict.get(step, Event)
    def get_form(self, step=None, data=None, files=None):
        template_name = "dining/event_form_%s.html" % step
        return form
    """

@staff_member_required
def event_detail(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render_to_response("dining/event_detail.html", {"event": event,}, context_instance=RequestContext(request))

@staff_member_required
def event_archives(request):
    events = Event.objects.all().order_by("-updated_on")
    return render_to_response("dining/event_archives.html", {"events": events,}, context_instance=RequestContext(request))


"""
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
"""
