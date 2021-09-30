# -*- coding: utf-8 -*-

import datetime
import os

from django.shortcuts import render
from djforms.scholars.models import Presentation


NOW  = datetime.datetime.now()
YEAR = int(NOW.year)


def alpha(request, template=None):
    presentations = Presentation.objects.filter(
        date_created__year=YEAR,
    ).filter(status=True).order_by('leader__last_name')
    if not template:
        template = 'scholars/print/pdf.html'
    return render(request, template, {'presentations': presentations})
