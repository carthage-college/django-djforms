# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djforms.lis.printjobs.forms import PrintRequestForm
from djtools.utils.mail import send_mail


@login_required
def index(request):
    if request.method == 'POST':
        form = PrintRequestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # save the files to `media` folder
            count = 1
            fs = FileSystemStorage(
                location='assets/files/lis/printjobs/',
                base_url='files/lis/printjobs/',
            )
            while count <= 3:
                phile = 'file{0}'.format(count)
                if data[phile]:
                    upload = data[phile]
                    filename = fs.save(upload.name, upload)
                    data[phile] = fs.url(filename)
                count += 1
            data['date'] = datetime.date.today()
            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = [settings.LIS_PRINT_REQUEST_EMAIL, data['email']]

            subject = '[Print Request]: {0} from the {1} Department'.format(
                data['name'], data['department'],
            )
            frum = data['email']
            send_mail(
                request,
                TO_LIST,
                subject,
                frum,
                'lis/printjobs/email.html',
                data,
                reply_to = [frum,],
                bcc = [settings.MANAGERS[0][1],],
            )
            return HttpResponseRedirect(reverse_lazy('lis_success'))
    else:
        form = PrintRequestForm()

    return render(request, 'lis/printjobs/form.html', {'form': form})
