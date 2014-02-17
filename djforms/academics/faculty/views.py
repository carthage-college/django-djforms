from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.academics.faculty.forms import DistinguishedTeachingAward

def distinguished_teaching_award(request):
    if request.method=='POST':
        form = DistinguishedTeachingAward(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bcc = settings.MANAGERS
            #recipient_list = ["larry@carthage.edu",]
            recipient_list = ["wwilliams@carthage.edu",]
            t = loader.get_template('academics/faculty/distinguished_teaching_award_email.html')
            c = RequestContext(request, {'object':data,})
            email = EmailMessage(("[Distinguished Teaching Award Nomination] %s submitted by %s" % (data['nominee'], data['name'])), t.render(c), data['email'], recipient_list, bcc, headers = {'Reply-To': data['email'],'From': data['email']})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/academics/faculty/teaching/success/')
    else:
        form = DistinguishedTeachingAward()
    return render_to_response("academics/faculty/distinguished_teaching_award_form.html", {"form": form,}, context_instance=RequestContext(request))
