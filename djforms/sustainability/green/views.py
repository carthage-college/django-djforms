from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djforms.sustainability.green.forms import PledgeForm
from djforms.sustainability.green.models import Pledge

from djtools.utils.mail import send_mail

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["csabar@carthage.edu","lhuaracha@carthage.edu",]
BCC = settings.MANAGERS

def pledge_form(request):
    '''
    simple form to submitting a pledge of fealty.
    '''

    user = request.user
    anon = True
    pledge = None

    if user.username:
        anon = False
        try:
            pledge = Pledge.objects.get(user=user)
        except:
            pledge = None

    if request.method=='POST':
        form = PledgeForm(request.POST)
        if form.is_valid() and not pledge:
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            subject = "[Sustainability Pledge] %s %s" % (
                user.first_name,user.last_name
            )
            send_mail(
                request,TO_LIST,subject,user.email,
                "sustainability/green/pledge_email.html", data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("pledge_form_success")
            )

    else:
        form = PledgeForm(initial={'user':user})

    return render_to_response(
        "sustainability/green/pledge_form.html",
        {"form": form, "anon": anon, "pledge":pledge,},
        context_instance=RequestContext(request)
    )

def pledge_archives(request):
    pledges = Pledge.objects.all().order_by("id")
    return render_to_response(
        "sustainability/green/pledge_archives.html",
        {"pledges": pledges,},
        context_instance=RequestContext(request)
    )
