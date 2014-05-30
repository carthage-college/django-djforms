from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from djforms.languages.studyabroad.forms import StudyAbroadForm

def study_abroad(request):
    if request.method == 'POST':
        form = StudyAbroadForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            to = ["ekulke@carthage.edu", "mkishline@gmail.com", cd['email']]
            bcc = settings.MANAGERS
            body =  'Name: ' + cd['name'] + '\n' + \
                    'E-mail: ' + cd['email'] + '\n' + \
                    'Phone: ' + cd['phone'] + '\n' + \
                    'Campus Box: ' + cd['campus_box'] + '\n' + \
                    'Majors: ' + cd['majors'] + '\n' + \
                    'Minors: ' + cd['minors'] + '\n' + \
                    'Parent Name: ' + cd['parent_name'] + '\n' + \
                    'Parent Phone: ' + cd['parent_phone'] + '\n' + \
                    'Parent Address: ' + cd['parent_address'] + '\n' + \
                    'Health Insurance: ' + cd['health_insurance'] + '\n' + \
                    'Preferred Language of instruction while abroad: ' + cd['preferred_language'] + '\n' + \
                    'Current or most recent language course: ' + cd['recent_course'] + '\n' + \
                    'Countries under consideration: ' + cd['desired_country'] + '\n' + \
                    'University/School Program abroad: ' + cd['school_program'] + '\n' + \
                    'Field of study while abroad: ' + cd['abroad_field'] + '\n' + \
                    'Year/Term of anticipated Study Abroad: ' + cd['abroad_year'] + '\n' + \
                    'Current year in college: ' + cd['current_year'] + '\n' + \
                    'Previous travel abroad: ' + str(cd['previous_travel']) + '\n' + \
                    'If yes, where?: ' + cd['traveled_places'] + '\n' + \
                    'Has Current Passport: ' + str(cd['passport']) + '\n' + \
                    'Expiration Date: ' + cd['passport_expiration'] + '\n' + \
                    'Housing Preferred: ' + cd['housing'] + '\n'
            email = EmailMessage(
                "Student Information for Study Abroad", body, cd['email'], to,
                bcc, headers = {'Reply-To': cd['email'],'From': cd['email']}
            )
            email.send(fail_silently=True)
            return HttpResponseRedirect(
                reverse_lazy("study_abroad_success")
            )
    else:
        form = StudyAbroadForm()
    return render_to_response(
        'languages/studyabroad/form.html',
        {'form': form}, context_instance=RequestContext(request)
    )
