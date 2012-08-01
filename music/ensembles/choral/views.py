from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djforms.music.ensembles.choral.forms import CandidateForm

import datetime

@login_required
def candidate(request):
    if request.method=='POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            # set the time slot active state to False
            candidate.time_slot.active = False
            candidate.time_slot.save()
            bcc = settings.MANAGERS
            #recipient_list = ["dshapovalov@carthage.edu","egarcianovelli@carthage.edu","pdennee@carthage.edu",]
            recipient_list = ["larry@carthage.edu",]
            t = loader.get_template('music/ensembles/choral/tryout_email.html')
            c = RequestContext(request, {'candidate':candidate,})
            email = EmailMessage(("[Choral Tryout Candidate] %s %s" % (candidate.user.first_name,candidate.user.last_name)), t.render(c), candidate.user.email, recipient_list, bcc, headers = {'Reply-To': candidate.user.email,'From': candidate.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/music/ensembles/choral/tryout/success/')
    else:
        form = CandidateForm()
    return render_to_response("music/ensembles/choral/tryout_form.html", {"form": form,}, context_instance=RequestContext(request))

