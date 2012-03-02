from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.astronomy.institute.forms import NightReportForm

def night_report(request):
    if request.method=='POST':
        form = NightReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bcc = settings.MANAGERS
            recipient_list = ["larry@carthage.edu",]
            #recipient_list = ["darion@carthage.edu",]
            t = loader.get_template('astronomy/institute/night_report_email.html')
            c = RequestContext(request, {'object':data,})
            email = EmailMessage(("[Griffin Observatory Night Report] Submitted by: %s of %s" % (object['name'],object['organization'])), t.render(c), object['email'], recipient_list, bcc, headers = {'Reply-To': object['email'],'From': object['email']})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/astronomy/institute/success/')
    else:
        form = NightReportForm()
    return render_to_response("astronomy/institute/night_report_form.html", {"form": form,}, context_instance=RequestContext(request))

