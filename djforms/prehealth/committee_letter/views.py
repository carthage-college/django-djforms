# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djforms.prehealth.committee_letter.forms import ApplicantForm
from djforms.prehealth.committee_letter.forms import RecommenderForm

from djtools.utils.mail import send_mail


@login_required
def applicant_form(request):

    if request.method == 'POST':
        form_app = ApplicantForm(request.POST, request.FILES)
        form_rec = RecommenderForm(request.POST, request.FILES)
        if form_app.is_valid():
            data = form_app.save(commit=False)
            data.created_by = request.user
            data.updated_by = request.user
            data.save()
            if not settings.DEBUG:
                TO_LIST.append(data.user.email)
                subject = u"[Committee Letter Applicant] {}: {}".format(
                    data.created_by.last_name, data.created_by.first_name
                ).encode('utf-8').strip()
                send_mail(
                    request, TO_LIST,
                    subject, data.created_by.email,
                    "prehealth/committee_letter/email.html", data,
                    settings.MANAGERS
                )
                return HttpResponseRedirect(
                    reverse('prehealth_committee_letter_applicant_success')
                )
            else:
                return render_to_response(
                    'prehealth/committee_letter/email.html',
                    {
                        'data': data,
                    },
                    context_instance=RequestContext(request)
                )
    else:
        form_app = ApplicantForm()
        form_rec = RecommenderForm()

    return render_to_response(
        'prehealth/committee_letter/form.html',
        {
            'form_app': form_app,
            'form_rec': form_rec,
        },
        context_instance=RequestContext(request)
    )
