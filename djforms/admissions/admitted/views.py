from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from djforms.admissions.admitted.forms import ChanceOfForm
from djtools.utils.mail import send_mail

import datetime

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["rob@carthage.edu",]
BCC = settings.MANAGERS

def chance_of_form(request):
    prospect_status = None
    if request.GET.keys():
        prospect_status = request.GET.keys()[0]
    if request.method=='POST':
        form = ChanceOfForm(request.POST)
        if form.is_valid():
            data = form.save()
            if data.gpa_scale == "100":
                data.adjusted_gpa = (float(data.gpa) - 60)/10
            else:
                data.adjusted_gpa = (float(data.gpa) * 4) / float(data.gpa_scale)
            data.save()
            subject = "Carthage, will I be admitted? (%s)" % (data.first_name)
            send_mail(
                request, TO_LIST, subject, data.email,
                "admissions/admitted/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("study_abroad_success")
            )
        else:
            prospect_status = request.POST.get("prospect_status")
    else:
        form = ChanceOfForm()
    return render_to_response(
        "admissions/admitted/form.html",
        {
            "form": form,
            "prospect_status":prospect_status
        }, context_instance=RequestContext(request))
