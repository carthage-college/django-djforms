from django.shortcuts import render

from djforms.scholars.models import Presentation

import datetime, os

NOW  = datetime.datetime.now()
YEAR = int(NOW.year)


def alpha(request, template=None):
    p = Presentation.objects.filter(date_updated__year=YEAR).filter(status=True)
    presentations = p.order_by('leader__last_name')

    if not template:
        template = 'scholars/print/pdf.html'

    return render(
        request, template, {'presentations': presentations,}
    )
