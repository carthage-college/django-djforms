from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djforms.biology.genomics.forms import PhageHunterForm
from djforms.biology.genomics.models import PhageHunter
from djtools.utils.mail import send_mail

def phage_hunter_form(request):
    if request.method=='POST':
        form = PhageHunterForm(request.POST)
        if form.is_valid():
            data = form.save()

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = settings.BIOLOGY_GENOMICS

            subject = "[Phage Hunters Application] {} {}".format(
                data.first_name, data.last_name
            )

            send_mail(
                request, TO_LIST, subject, data.email,
                "biology/genomics/phage_hunter_email.html", data,
                settings.MANAGERS
            )

            return HttpResponseRedirect(
                reverse_lazy("phage_hunters_success")
            )
    else:
        form = PhageHunterForm()
    return render_to_response(
        "biology/genomics/phage_hunter_form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

@staff_member_required
def phage_hunter_detail(request, pid):
    applicant = get_object_or_404(PhageHunter, id=pid)
    return render_to_response(
        "biology/genomics/phage_hunter_detail.html",
        {"applicant": applicant,},
        context_instance=RequestContext(request)
    )

@staff_member_required
def phage_hunter_archives(request):
    applicants = PhageHunter.objects.all().order_by("-created_at")
    return render_to_response(
        "biology/genomics/phage_hunter_archives.html",
        {"applicants": applicants,},
        context_instance=RequestContext(request)
    )
