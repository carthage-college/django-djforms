from django.conf import settings
from djtools.utils.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
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
            subject = "[CIA Night Report] Submitted by: %s of %s" %
                (data['name'],data['organization'])
            send_mail(
                request, TO_LIST, subject, data['email'],
                "astronomy/institute/night_report_email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("cia_night_report_success")
            )
    else:
        form = NightReportForm()
    return render_to_response(
        "astronomy/institute/night_report_form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

def evaluation(request):
    if request.method=='POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = "[CIA Evaluation] Submitted by: %s" % data['name']
            send_mail(
                request, TO_LIST, subject, data['email'],
                "astronomy/institute/evaluation_email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("cia_evaluation_success")
            )
    else:
        form = EvaluationForm()
    return render_to_response(
        "astronomy/institute/evaluation_form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )
