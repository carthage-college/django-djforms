from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader

from djforms.alumni.msw.forms import ReunionContactForm
from djforms.alumni.msw.models import ReunionContact

def reunion_contact_form(request):
    if request.method=='POST':
        form = ReunionContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            bcc = settings.MANAGERS
            recipient_list = ["dfrancz@luc.edu",]
            t = loader.get_template('alumni/msw/reunion_contact_email.html')
            c = RequestContext(request, {'contact':contact,})
            email = EmailMessage(("[MSW Reunion Contact] %s %s" % (contact.first_name,contact.last_name)), t.render(c), contact.email, recipient_list, bcc, headers = {'Reply-To': contact.email,'From': contact.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/alumni/msw/reunion/success/')
    else:
        form = ReunionContactForm()
    return render_to_response("alumni/msw/reunion_contact_form.html", {"form": form,}, context_instance=RequestContext(request))

def reunion_contact_detail(request, id):
    contact = get_object_or_404(ReunionContact,id=id)
    return render_to_response("alumni/msw/reunion_contact_detail.html", {"contact": contact,}, context_instance=RequestContext(request))

def reunion_contact_archives(request):
    contacts = ReunionContact.objects.all().order_by("last_name")
    return render_to_response("alumni/msw/reunion_contact_archives.html", {"contacts": contacts,}, context_instance=RequestContext(request))

