#!/usr/bin/python

from django.conf import settings

from djforms.scholars.models import Presentation

from djtools.fields import TODAY

YEAR = int(TODAY.year)

prez = Presentation.objects.filter(date_updated__year=YEAR)

# list for failed uploads
#bunk = [ ]
#if s.mugshot in bunk:
#    print s.first_name, s.last_name

for p in prez:
    for s in p.presenters.all():
        if s.mugshot:
            print s.mugshot

