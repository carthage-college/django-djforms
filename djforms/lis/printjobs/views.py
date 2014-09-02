from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader
from djforms.lis.printjobs.forms import PrintRequestForm
from django.contrib.auth.decorators import login_required

import datetime

@login_required
def print_request(request):
    if request.method=='POST':
        form = PrintRequestForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            t = loader.get_template('lis/printjobs/email.html')
            c = RequestContext(
                request, {
                    'data':cd,'date':datetime.date.today()
                }
            )
            BCC = settings.MANAGERS
            TO_LIST = ["mrprintreqs@carthage.edu",cd['email']]
            email = EmailMessage(
                "[LIS Print Request]: %s from the %s Department" % (
                    cd['name'],cd['department']
                ), t.render(c), cd['email'], TO_LIST, BCC,
                headers = {'Reply-To': cd['email'],'From': cd['email']}
            )
            email.content_subtype = "html"
            for field, value in request.FILES.items():
                email.attach(value.name, value.read(), value.content_type)
            email.send(fail_silently=False)
            return HttpResponseRedirect(
                reverse_lazy("lis_success")
            )
    else:
        form = PrintRequestForm()
    return render_to_response(
        "lis/printjobs/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )
