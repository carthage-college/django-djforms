from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from djforms.lacrossegolfinvite.forms import LacrosseGolfInviteForm

def lacrosse_golf_invite_form(request):
    if request.method == 'POST':
        form = LacrosseGolfInviteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            bcc = settings.MANAGERS
            to = ['larry@carthage.edu', cd['email']]
            body =  'Name:..... ' + cd['first_name'] + ' ' + cd['last_name'] + '\n' + \
                    'Address:.. ' + cd['address'] + '\n' + \
                    'City:..... ' + cd['city'] + '\n' + \
                    'Zip:...... ' + cd['zip'] + '\n' + \
                    'Phone:.... ' + cd['phone'] + '\n' + \
                    'E-mail:... ' + cd['email'] + '\n' + \
                    'Nimber attending Golf and Dinner:.. ' + str(cd['num_golf_and_dinner']) + '\n' + \
                    'Number attending Dinner only:...... ' + str(cd['num_dinner_only']) + '\n' + \
                    'Amount To Be Enclosed:............ $' + str(cd['amount_due']) + '\n' + \
                    'Golfing Foursome E-mail 1: ' + cd['email_1'] + '\n' + \
                    'Golfing Foursome E-mail 2: ' + cd['email_2'] + '\n' + \
                    'Golfing Foursome E-mail 3: ' + cd['email_3'] + '\n' + \
                    'Golfing Foursome E-mail 4: ' + cd['email_4'] + '\n' + \
                    'Place user in Golfing Foursome: ' + cd['place_str'] + '\n' + \
                    'User is attending?: ' + cd['attend_str'] + '\n'
            email = EmailMessage("Lacrosse Golf Invite Form Submission", body, cd['email'], to, bcc, headers = {'Reply-To': cd['email'],'From': cd['email']})
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/lacrossegolfinvite/request-sent')
    else:
        form = LacrosseGolfInviteForm()
    return render_to_response('lacrossegolfinvite/lacrosse_golf_invite_form.html', {'form': form}, context_instance=RequestContext(request))
