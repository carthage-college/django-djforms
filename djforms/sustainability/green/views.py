from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djforms.sustainability.green.forms import PledgeForm
from djforms.sustainability.green.models import Pledge

from djtools.utils.mail import send_mail

def pledge_form(request):
    '''
    simple form to submitting a pledge of fealty.
    '''
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = settings.SUSTAINABILITY_EMAIL_LIST
    BCC = settings.MANAGERS

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
            subject = "[Sustainability Pledge] {} {}".format(
                user.first_name,user.last_name
            )
            send_mail(
                request,TO_LIST,subject,user.email,
                'sustainability/green/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('green_pledge_success')
            )

    else:
        form = PledgeForm(initial={'user':user})

    return render(
        'sustainability/green/form.html',
        {'form': form, 'anon': anon, 'pledge':pledge,}
    )


def pledge_archives(request):
    pledges = Pledge.objects.all().order_by('id')

    return render(
        request, 'sustainability/green/archives.html',
        {'pledges': pledges,}
    )
