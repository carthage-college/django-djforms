from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.files.base import ContentFile

from djforms.alumni.distinguished.forms import NomineeForm, NominatorForm

import datetime

def nomination_form(request):
    if request.method=='POST':
        nominee_form = NomineeForm(request.POST,prefix="nominee")
        nominator_form = NominatorForm(request.POST,prefix="nominator")
        if nominee_form.is_valid() and nominator_form.is_valid():
            nominee = nominee_form.cleaned_data
            nominator = nominator_form.cleaned_data
            bcc = settings.MANAGERS
            to = ["alumnioffice@carthage.edu"]
            #to = ["larry@carthage.edu"]
            t = loader.get_template('alumni/distinguished/nomination_email.txt')
            c = RequestContext(request, {'nominee':nominee,'nominator':nominator,})
            email = EmailMessage("Distinguished Alumni Award Nomination: %s" % nominee['name'], t.render(c), nominator['email'], to, bcc, headers = {'Reply-To': nominator['email'],'From': nominator[ 'email']})
            email.content_subtype = "html"
            email.send(fail_silently=False)
            return HttpResponseRedirect('/alumni/distinguished-alumni/nomination/success/')
    else:
        nominee_form = NomineeForm(prefix="nominee")
        nominator_form = NominatorForm(prefix="nominator")
    return render_to_response("alumni/distinguished/nomination_form.html", {"nominee_form":nominee_form,"nominator_form":nominator_form,}, context_instance=RequestContext(request))
