from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
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
            bcc = settings.MANAGERS
            to = ["mrprintreqs@carthage.edu",cd['email']]
            t = loader.get_template('lis/printjobs/request_email.txt')
            c = RequestContext(request, {'data':cd,'date':datetime.date.today()})
            email = EmailMessage("[LIS Print Request]: %s from the %s Department" % (cd['name'],cd['department']), t.render(c), cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.content_subtype = "html"
            attachments = request.FILES
            for field, value in request.FILES.items():
                email.attach(value.name, value.read(), value.content_type)
            email.send(fail_silently=False)
            return HttpResponseRedirect('/library/success/')
    else:
        form = PrintRequestForm()
    return render_to_response("lis/printjobs/request_form.html", {"form": form,}, context_instance=RequestContext(request))
