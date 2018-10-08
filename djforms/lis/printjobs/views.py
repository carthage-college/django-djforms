from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djforms.lis.printjobs.forms import PrintRequestForm

from djtools.utils.mail import send_mail

import datetime


@login_required
def index(request):
    if request.method=='POST':
        form = PrintRequestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['date'] = datetime.date.today()

            BCC = settings.MANAGERS
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [settings.LIS_PRINT_REQUEST_EMAIL, data['email']]

            subject = "[Print Request]: {} from the {} Department".format(
                data['name'],data['department']
            )

            send_mail(
                request, TO_LIST,
                subject, data['email'],
                'lis/printjobs/email.html', data, BCC, attach=True
            )

            return HttpResponseRedirect(
                reverse_lazy('lis_success')
            )
    else:
        form = PrintRequestForm()

    return render(
        request, 'lis/printjobs/form.html', {'form': form,}
    )
