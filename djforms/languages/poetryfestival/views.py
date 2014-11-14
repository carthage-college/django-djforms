from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djforms.languages.poetryfestival.forms import SignupForm

from djtools.utils.mail import send_mail

@login_required
def signup_form(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = ['scyganiak@carthage.edu', cd['email']]

            subject = "Poetry Festival Signup Form: %s %s" % (
                cd['first_name'], cd['last_name']
            )

            send_mail(
                request, TO_LIST, subject, cd['email'],
                "languages/poetryfestival/email.html", cd, settings.MANAGERS
            )

            return HttpResponseRedirect(
                reverse_lazy("poetry_festival_success")
            )
    else:
        form = SignupForm()
    return render_to_response(
        'languages/poetryfestival/form.html',
        {'form': form}, context_instance=RequestContext(request)
    )
