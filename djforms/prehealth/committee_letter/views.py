# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from djforms.prehealth.committee_letter.models import Applicant, Evaluation
from djforms.prehealth.committee_letter.models import Recommendation
from djforms.prehealth.committee_letter.forms import ApplicantForm
from djforms.prehealth.committee_letter.forms import EvaluationForm

from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djtools.decorators.auth import group_required


def _to_list(data):
    '''
    private function that creates an email distribution list
    with appropriate pre-health folks based on the typs of programs to
    which the student has indicated s/he will be applying
    '''

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
    return to


@login_required
def evaluation_form(request, aid):
    '''
    Evaluation and recommendation form, submitted after student submits
    her committee letter application
    '''

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

                # obtain the distribution list w/ appropriate pre-health folks
                to_list = _to_list(app)
                # subject for email
                subject = u"[Committee Letter Evaluation] For {}, {} by {}, {}".format(
                    app.created_by.last_name, app.created_by.first_name,
                    data.created_by.last_name, data.created_by.first_name
                ).encode('utf-8').strip()
                if not settings.DEBUG:
                    # send email to pre-health folks
                    send_mail(
                        request, to_list, subject, data.created_by.email,
                        'prehealth/committee_letter/evaluation/email.html',
                        data, settings.MANAGERS
                    )

                return HttpResponseRedirect(
                    reverse_lazy(
                        'prehealth_committee_letter_evaluation_success'
                    )
                )
        else:
            form = EvaluationForm()

        return render(
            request, 'prehealth/committee_letter/evaluation/form.html',
            {
                'form': form,'app':app,
            }
        )

    else:
        # something is rotten in denmark
        return HttpResponseRedirect(
            reverse_lazy('access_denied')
        )


@login_required
def applicant_form(request):
    '''
    Committee letter application form submitted by student
    '''

    copies=1
    recommendations = ['']
    if request.method == 'POST':
        form_app = ApplicantForm(request.POST, request.FILES)

        name = request.POST.getlist('name[]')
        email = request.POST.getlist('email[]')
        recommendations = []
        # len could use any of the above 4 lists
        copies = len(email)
        for i in range (1, copies):
            if email[i] and name[i]:
                recommendations.append({
                    'email':email[i],
                    'name':name[i],
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
                r = Recommendation(
                    applicant = data,
                    name = rec['name'],
                    email = rec['email']
                )
                r.save()

            # subject for emails
            subject = u"[Committee Letter Applicant] {}, {}".format(
                data.created_by.last_name, data.created_by.first_name
            ).encode('utf-8').strip()

            # obtain the distribution list with appropriate pre-health folks
            to_list = _to_list(data)

            # send email to pre-health folks
            send_mail(
                request, to_list, subject, data.created_by.email,
                'prehealth/committee_letter/email.html', data,
                settings.MANAGERS
            )

            # send email to each of the recommendation contacts
            recs = data.prehealth_committee_letter_recommendation_applicant.all()
            for rec in recs:
                data.name = rec.name
                send_mail(
                    request, [rec.email,], subject, settings.PREHEALTH_MD,
                    'prehealth/committee_letter/email_faculty.html', data,
                    settings.MANAGERS
                )

            return HttpResponseRedirect(
                reverse_lazy('prehealth_committee_letter_applicant_success')
            )

        else:

            if copies < 3:
                messages.add_message(
                    request, messages.ERROR,
                    '''
                    You must submit at least 3 recommendation contacts
                    ''',
                    extra_tags='danger'
                )
                if copies < 1:
                    copies = 1
                    recommendations.append({
                        'email':'',
                        'name':'',
                    })
                else:
                    copies = len(recommendations)

                # needs django 1.8+
                form_app.add_error(
                    None, "You must submit at least 1 recommendation contact"
                )
    else:
        form_app = ApplicantForm()

    return render(
        request, 'prehealth/committee_letter/form.html',
        {
            'form_app': form_app,
            'recommendations': recommendations,
            'copies': copies
        }
    )


@group_required('SuperStaff')
def applicant_detail(request, aid):
    '''
    Simple view to display the application detail
    '''

    app = get_object_or_404(Applicant, id=aid)

    template_name = 'prehealth/committee_letter/detail.html'

    return render(
        request, template_name, {'data': app,'detail':True}
    )

