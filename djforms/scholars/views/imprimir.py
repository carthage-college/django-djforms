from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.scholars.models import Presentation

import datetime, os

NOW  = datetime.datetime.now()
YEAR = int(NOW.year)

def alpha(request, template=None):
    p = Presentation.objects.filter(date_updated__year=YEAR)
    presentations = p.order_by('leader__last_name')

    if not template:
        template = "scholars/print/pdf.html"
    return render_to_response (
        template, {"presentations": presentations,},
        context_instance=RequestContext(request)
    )
