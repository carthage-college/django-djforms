from django.conf import settings
from django.http import HttpResponseRedirect
from djforms.core.views import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.astronomy.institute.forms import NightReportForm, EvaluationForm

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["darion@carthage.edu",]
BCC = settings.MANAGERS

def night_report(request):
    if request.method=='POST':
        form = NightReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = "[Griffin Observatory Night Report] Submitted by: %s of %s" % (data['name'],data['organization'])
            send_mail(request, TO_LIST, subject, data['email'], "astronomy/institute/night_report_email.html", data, BCC)
            return HttpResponseRedirect('/forms/astronomy/institute/night-report/success/')
    else:
        form = NightReportForm()
    return render_to_response("astronomy/institute/night_report_form.html", {"form": form,}, context_instance=RequestContext(request))

def evaluation(request):
    if request.method=='POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = "[Griffin Observatory Evaluation] Submitted by: %s" % data['name']
            send_mail(request, TO_LIST, subject, data['email'], "astronomy/institute/evaluation_email.html", data, BCC)
            return HttpResponseRedirect('/forms/astronomy/institute/evaluation/success/')
    else:
        form = EvaluationForm()
    return render_to_response("astronomy/institute/evaluation_form.html", {"form": form,}, context_instance=RequestContext(request))

