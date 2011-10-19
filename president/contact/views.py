from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.president.contact.forms import ContactForm

def contact_form(request):

    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            bcc = settings.MANAGERS
            #to = ["presidentsearch@carthage.edu",]
            to = ["skirk@carthage.edu",]
            t = loader.get_template('president/contact/email.html')
            c = RequestContext(request, {'data':cd,})
            email = EmailMessage(("[Presidential Search Comments] %s" % cd["name"]), t.render(c), cd["email"], to, bcc, headers = {'Reply-To': cd["email"],'From': cd["email"]})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/president/contact/success')
    else:
        form = ContactForm()
    return render_to_response("president/contact/contact_form.html", {"form": form,'type':type}, context_instance=RequestContext(request))

