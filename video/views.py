from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import get_model
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djforms.video.forms import ContestForm
from djforms.video.models import Contest
from tagging.models import Tag, TaggedItem

@login_required
def contest_form(request):
    if request.method=='POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.user = request.user
            contest.updated_by = request.user
            contest.tags = "Lives Worth Living,"
            contest.save()
            bcc = settings.MANAGERS
            recipient_list = ["larry@carthage.edu"]
            t = loader.get_template('video/contest_email.html')
            c = RequestContext(request, {'data':contest,'user':request.user,})
            email = EmailMessage(("[Video Contest Submission] %s: by %s %s" % (contest.title,request.user.first_name,request.user.last_name)), t.render(c), request.user.email, recipient_list, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/video/success')
    else:
        form = ContestForm()
    return render_to_response("video/contest_form.html", {"form": form,}, context_instance=RequestContext(request))

def contest_archives(request, tag):
    model = get_model('video','contest')
    tag = Tag.objects.get(name=tag)
    videos = TaggedItem.objects.get_by_model(model, tag)
    return render_to_response("video/contest_archives.html", {"videos": videos,}, context_instance=RequestContext(request))
