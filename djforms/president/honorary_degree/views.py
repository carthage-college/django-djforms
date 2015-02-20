# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djforms.president.honorary_degree.forms import NominationForm
from djtools.utils.mail import send_mail

import datetime

def nomination_form(request):
    if request.method=='POST':
        nom_form = NominationForm(request.POST, request.FILES)
        if nom_form.is_valid():
            data = nom_form.save()
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [settings.HONORARY_DEGREE_NOMINATION_EMAIL]
            subject = "Honorary Degree Nomination: {} {}".format(
                data.candidate_first_name, data.candidate_last_name
            )
            send_mail(
                request, TO_LIST,
                subject, data.email,
                "president/honorary_degree/email.html", data,
                settings.MANAGERS
            )
            return HttpResponseRedirect(
                reverse_lazy("honorary_degree_nomination_success")
            )
    else:
        nom_form = NominationForm()
    return render_to_response(
        "president/honorary_degree/form.html",
        {"form":nom_form,},
        context_instance=RequestContext(request)
    )
