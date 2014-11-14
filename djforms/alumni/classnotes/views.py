from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader

from djforms.alumni.classnotes.forms import ContactForm
from djforms.alumni.classnotes.models import Contact
from djtools.utils.mail import send_mail

from honeypot.decorators import check_honeypot

import datetime

@check_honeypot
def contact(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = ["dmoore2@carthage.edu",]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if contact.email:
                email = contact.email
            subject = "[Alumni Class Notes] %s %s" % (
                contact.first_name,contact.last_name
            )
            send_mail(
                request,TO_LIST, subject, email,
                "alumni/classnotes/email.html", contact, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("classnotes_success")
            )
    else:
        form = ContactForm()
    manager = request.user.has_perm('classnotes.change_contact')
    return render_to_response(
        "alumni/classnotes/form.html",
        {"form": form,"manager":manager,},
        context_instance=RequestContext(request)
    )

def archives(request, year=None):
    """
    decade based archives
    """
    if year:
        year = int(year)
    else:
        year = 2010

    ns = Contact.objects.exclude(pubstatus=False).exclude(category='Death Announcement').exclude(classnote__exact='None')
    notes = ns.filter(classyear__range=[year,year+9]).order_by("-classyear", "last_name")
    manager = request.user.has_perm('classnotes.change_contact')

    return render_to_response(
        "alumni/classnotes/archives.html", {
            "notes": notes,"year":year,"manager":manager,
        },
        context_instance=RequestContext(request)
    )

def screenscrape(request):
    ns = Contact.objects.exclude(carthaginianstatus=True)
    notes = ns.order_by("classyear", "last_name")
    manager = request.user.has_perm('classnotes.change_contact')

    return render_to_response("alumni/classnotes/archives.html", {
        "notes": notes,"title":"Carthaginian","manager":manager,
    }, context_instance=RequestContext(request))

def obits(request):
    obs = Contact.objects.filter(category="Death Announcement")
    notes = obs.order_by("classyear", "last_name")

    return render_to_response("alumni/classnotes/archives.html", {
        "notes": notes,"title":"In Memoriam",
    }, context_instance=RequestContext(request))


