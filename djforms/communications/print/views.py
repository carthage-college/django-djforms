from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from djforms.communications.print.forms import RequestForm
from djtools.utils.mail import send_mail

def form(request):
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.save()
            
            subject = "Carthage, will I be admitted? (%s)" % (data.first_name)
            send_mail(
                request, TO_LIST, subject, data.email,
                "admissions/admitted/email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("admitted_success")
            )
        else:
            prospect_status = request.POST.get("prospect_status")
    else:
        form = ChanceOfForm()
    return render_to_response(
        "admissions/admitted/form.html",
        {
            "form": form            
        }, context_instance=RequestContext(request))
