#!/usr/bin/python

from djforms.scholars.models import Presentation

prez = Presentation.objects.all()

for p in prez:
    p.date_updated = p.date_created
    p.save()
