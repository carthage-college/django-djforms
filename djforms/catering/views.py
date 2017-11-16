from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.contrib.admin.views.decorators import staff_member_required

from djforms.catering.forms import EventForm1, EventForm2, EventForm3
from djforms.catering.forms import EventForm4, EventForm5
from djforms.catering.models import Event

from djtools.utils.mail import send_mail

import os.path

storage_location = os.path.join(settings.MEDIA_ROOT, 'files/catering/temp/')
storage = FileSystemStorage(location=storage_location)

class CateringEventWizard(SessionWizardView):
    """
    Form wizard view for processing the event steps
    """
    file_storage = storage
    template_name = 'catering/event_form_wizard.html'

    def done(self, form_list, **kwargs):
        # keeps python from concatenating other sessions
        if settings.DEBUG:
            TO_LIST = [settings.SERVER_EMAIL]
        else:
            TO_LIST = list(settings.CATERING_TO_LIST)

        event = Event()
        xfields = {'open_to':'', 'room_set_up':'', 'beverages':''}
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
        # send mail
        email = event.user.email
        TO_LIST.append(email)
        subject = "[Event Request Form] {}: {} {}".format(
            event.department,event.user.first_name,event.user.last_name
        )
        send_mail(
            self.request, TO_LIST, subject, email,
            'catering/event_email.html', {'event':event,},
            settings.MANAGERS
        )

        return HttpResponseRedirect(
            reverse_lazy('catering_event_success')
        )

    def get_form(self, step=None, data=None, files=None):
        form = super(CateringEventWizard, self).get_form(step, data, files)
        #template_name = 'catering/event_form_{}.html'.format(step)
        #template_name = 'catering/event_form_wizard.html'
        return form


@staff_member_required
def event_detail(request, eid):
    event = get_object_or_404(Event, id=eid)

    return render(
        request, 'catering/event_detail.html', {'event': event,}
    )


@staff_member_required
def event_archives(request):
    events = Event.objects.all().order_by('-updated_on')

    return render(
        request, 'catering/event_archives.html',
        {'events': events,}
    )
