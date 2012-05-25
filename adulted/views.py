from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from djforms.adulted.forms import *

def admissions_form(request):
    if request.method=='POST':
        contact_form = ContactForm(request.POST)
        personal_form = PersonalForm(request.POST)
        employment_form = EmploymentForm(request.POST)
        education_form = EducationForm(request.POST)
        if contact_form.is_valid() and personal_form.is_valid() and employment_form.is_valid() and education_form.is_valid():
            contact = contact_form.cleaned_data
            personal = personal_form.cleaned_data
            employment = employment_form.cleaned_data
            education = education_form.cleaned_data
            bcc = settings.MANAGERS
            #recipient_list = ["tom@carthage.edu","brichards@carthage.edu","jweiser@carthage.edu",]
            recipient_list = [settings.SERVER_EMAIL,]
            t = loader.get_template('adulted/admissions_email.html')
            c = RequestContext(request, {'contact':contact,'personal':personal,'employment':employment,'education':education,})
            email = EmailMessage(("[Adult Education Application] %s, %s" % (contact['last_name'],contact['first_name'])), t.render(c), contact['email'], recipient_list, bcc, headers = {'Reply-To': contact['email'],'From': contact['email']})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/adulted/admissions/success/')
    else:
        contact_form = ContactForm()
        personal_form = PersonalForm()
        employment_form = EmploymentForm()
        education_form = EducationForm()
    return render_to_response("adulted/admissions_form.html", {"contact_form": contact_form,"personal_form":personal_form,"employment_form":employment_form,"education_form":education_form,}, context_instance=RequestContext(request))
