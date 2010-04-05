from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from djforms.poetryfestival.forms import SignupForm

def signup_form(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #to = ['scyganiak@carthage.edu',cd['email']]
            to = ['skirk@carthage.edu']
            bcc = settings.MANAGERS
            body =  'Name: ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' +\
                    'Email: ' + cd['email'] + '\n' +\
                    'Title of the Poem: ' + cd['poem_title'] + '\n' +\
                    'Author of the Poem: ' + cd['poem_author'] + '\n' +\
                    'Language of the Poem: ' + cd['poem_language'] + '\n' +\
                    'Time slot preference: \n\n' + cd['time_slot'] + '\n\n' +\
                    'Questions or Comments:  \n\n' + cd['comments'] + '\n'

            email = EmailMessage("Poetry Festival Signup Form: %s %s" % (cd['first_name'],cd['last_name']), body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/poetry-festival/data-entered')
    else:
        form = SignupForm()
    return render_to_response('poetryfestival/signup_form.html', {'form': form}, context_instance=RequestContext(request))
