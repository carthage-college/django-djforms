# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from djforms.prehealth.committee_letter.forms import ApplicantForm
from djforms.prehealth.committee_letter.forms import EvaluationForm
from djforms.prehealth.committee_letter.models import Applicant
from djforms.prehealth.committee_letter.models import Evaluation
from djforms.prehealth.committee_letter.models import Recommendation
from djtools.decorators.auth import group_required
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


def _to_list(data):
    """
    Private function that creates an email distribution list.

    Populated with appropriate pre-health folks based on the typs of programs
    to which the student has indicated s/he will be applying.
    """
    to = []
    do = settings.PREHEALTH_DO
    dr = settings.PREHEALTH_MD
    for prog in data.programs_apply.all():
        if 'M.D.' in prog.name:
            # M.D. and /M.D./Ph.D. programs
            if dr not in to:
                to.append(dr)
        else:
            # D.O. and D.D.S programs
            if do not in to:
                to.append(do)
    to.append(settings.PREHEALTH_CC)
    return to


@login_required
def evaluation_form(request, aid):
    """
    Display the Evaluation and recommendation form.

    Submitted after student submits her committee letter application.
    """
    user = request.user
    app = get_object_or_404(Applicant, id=aid)
    # check if our user is in the list of recommendation contacts
    access = False
    for rec in app.prehealth_committee_letter_recommendation_applicant.all():
        if rec.email.strip() == user.email:
            access = True
            break

    if access or in_group(request.user, 'SuperStaff'):
        if request.method == 'POST':
            form = EvaluationForm(request.POST, request.FILES)
            if form.is_valid():
                # save our data
                data = form.save(commit=False)
                data.applicant = app
                data.created_by = request.user
                data.updated_by = request.user
                data.save()
                if settings.DEBUG:
                    to_list = [settings.SERVER_EMAIL]
                else:
                    # obtain the distribution list with appropriate recipients
                    to_list = _to_list(app)
                # subject for email
                subject = '[Committee Letter Evaluation] For {0}, {1} by {2}, {3}'.format(
                    app.created_by.last_name,
                    app.created_by.first_name,
                    data.created_by.last_name,
                    data.created_by.first_name,
                ).encode('utf-8').strip()
                # send email to pre-health folks
                send_mail(
                    request,
                    to_list,
                    subject,
                    data.created_by.email,
                    'prehealth/committee_letter/evaluation/email.html',
                    data,
                    [settings.MANAGERS[0][1]],
                )
                return HttpResponseRedirect(
                    reverse_lazy('prehealth_committee_letter_evaluation_success'),
                )
        else:
            form = EvaluationForm()

        return render(
            request,
            'prehealth/committee_letter/evaluation/form.html',
            {'form': form,'app':app},
        )
    else:
        # something is rotten in denmark
        return HttpResponseRedirect(reverse_lazy('access_denied'))


@login_required
def applicant_form(request):
    """Committee letter application form submitted by students."""
    copies = 1
    recommendations = ['']
    if request.method == 'POST':
        form_app = ApplicantForm(request.POST, request.FILES)
        name = request.POST.getlist('name[]')
        email = request.POST.getlist('email[]')
        recommendations = []
        # len could use any of the above 4 lists
        copies = len(email)
        for index in range (1, copies):
            if email[index] and name[index]:
                recommendations.append({
                    'email':email[index],
                    'name':name[index],
                })
        copies = len(recommendations)
        if copies >= 3 and form_app.is_valid():
            # save our new applicant object
            data = form_app.save(commit=False)
            data.created_by = request.user
            data.updated_by = request.user
            data.save()
            # m2m save for programs_apply GenericChoice relationships
            form_app.save_m2m()
            # update user profile
            profile = data.created_by.userprofile
            profile.city = request.POST['city']
            profile.state = request.POST['state']
            profile.phone = request.POST['phone']
            profile.save()
            # create our new recommendation objects
            for rec in recommendations:
                recommendation = Recommendation(
                    applicant = data,
                    name = rec['name'],
                    email = rec['email'],
                )
                recommendation.save()
            # subject for emails
            subject = '[Committee Letter Applicant] {0}, {1}'.format(
                data.created_by.last_name, data.created_by.first_name,
            ).strip()
            # obtain the distribution list with appropriate pre-health folks
            to_list = _to_list(data)
            # send email to pre-health folks
            send_mail(
                request,
                to_list,
                subject,
                data.created_by.email,
                'prehealth/committee_letter/email.html',
                data,
                [settings.MANAGERS[0][1]],
            )
            # send email to each of the recommendation contacts
            recs = data.prehealth_committee_letter_recommendation_applicant.all()
            for rec in recs:
                data.name = rec.name
                send_mail(
                    request,
                    [rec.email],
                    subject,
                    settings.PREHEALTH_MD,
                    'prehealth/committee_letter/email_faculty.html',
                    data,
                    [settings.MANAGERS[0][1]],
                )
            return HttpResponseRedirect(
                reverse_lazy('prehealth_committee_letter_applicant_success'),
            )
        else:
            if copies < 3:
                messages.add_message(
                    request, messages.ERROR,
                    'You must submit at least 3 recommendation contacts',
                    extra_tags='danger',
                )
                if copies < 1:
                    copies = 1
                    recommendations.append({'email': '', 'name': ''})
                else:
                    copies = len(recommendations)
                form_app.add_error(
                    None, "You must submit at least 1 recommendation contact",
                )
    else:
        form_app = ApplicantForm()

    return render(
        request,
        'prehealth/committee_letter/form.html',
        {
            'form_app': form_app,
            'recommendations': recommendations,
            'copies': copies,
        }
    )


@group_required('SuperStaff')
def applicant_detail(request, aid):
    """Simple view to display the application detail."""
    app = get_object_or_404(Applicant, id=aid)
    template_name = 'prehealth/committee_letter/detail.html'
    return render(request, template_name, {'data': app, 'detail': True})
