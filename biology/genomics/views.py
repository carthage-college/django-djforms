from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.admin.views.decorators import staff_member_required

from djforms.biology.genomics.forms import PhageHunterForm
from djforms.biology.genomics.models import PhageHunter

def phage_hunter_form(request):
    if request.method=='POST':
        form = PhageHunterForm(request.POST)
        if form.is_valid():
            data = form.save()
            bcc = settings.MANAGERS
            #recipient_list = ["larry@carthage.edu",]
            recipient_list = ["larry@carthage.edu",]
            t = loader.get_template('biology/genomics/phage_hunter_email.html')
            c = RequestContext(request, {'applicant':data,})
            email = EmailMessage(("[Phage Hunters Application] %s %s" % (data.first_name,data.last_name)), t.render(c), data.email, recipient_list, bcc, headers = {'Reply-To': data.email,'From': data.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/biology/genomics/phage-hunters/success/')
    else:
        form = PhageHunterForm()
    return render_to_response("biology/genomics/phage_hunter_form.html", {"form": form,}, context_instance=RequestContext(request))

@staff_member_required
def phage_hunter_detail(request, id):
    applicant = get_object_or_404(PhageHunter, id=id)
    return render_to_response("biology/genomics/phage_hunter_detail.html", {"applicant": applicant,}, context_instance=RequestContext(request))

@staff_member_required
def phage_hunter_archives(request):
    applicants = PhageHunter.objects.all().order_by("-created_on")
    return render_to_response("biology/genomics/phage_hunter_archives.html", {"applicants": applicants,}, context_instance=RequestContext(request))

