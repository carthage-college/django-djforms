from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.alumni.classnotes.forms import ContactForm
from djforms.alumni.classnotes.models import Contact
from djtools.utils.mail import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["dmoore2@carthage.edu","eyoung@carthage.edu"]
BCC = settings.MANAGERS

def contact(request):
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if contact.email:
                email = contact.email
            subject = "[Alumni Class Notes] %s %s" % (contact.first_name,contact.last_name)
            send_mail(
                request,TO_LIST, subject, email,
                "alumni/classnotes/email.html", contact, BCC
            )
            return HttpResponseRedirect('/forms/alumni/classnotes/success/')
    else:
        form = ContactForm()
    manager = request.user.has_perm('classnotes.change_contact')
    return render_to_response("alumni/classnotes/form.html",
        {"form": form,"manager":manager,}, context_instance=RequestContext(request))

def archives(request, year=None):
    """
    decade based archives
    """
    if year:
        year = int(year)
    else:
        year = 2010

    ns = Contact.objects.exclude(pubstatus=False).exclude(classnote__exact='None')
    notes = ns.filter(classyear__range=[year,year+9]).order_by("-classyear", "last_name")
    manager = request.user.has_perm('classnotes.change_contact')

    return render_to_response("alumni/classnotes/archives.html", {
        "notes": notes,"year":year,"manager":manager,
    }, context_instance=RequestContext(request))
