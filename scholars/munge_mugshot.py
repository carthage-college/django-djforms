#!/usr/bin/python

from djforms.scholars.models import Presentation

import os, uuid

prez = Presentation.objects.all()

root_path = "/data2/django_projects/djforms/assets/"
upload_dir = "files/scholars/mugshots/"

for p in prez:
    for s in p.presenters.all():
        if s.mugshot:
            orig         = root_path + s.mugshot.name
            new_filename = "%s%s_%s_%s.jpg" % (upload_dir, s.last_name, s.first_name, uuid.uuid4().hex)
            new          = root_path + new_filename
            #print new_filename, s.mugshot.name
            #print new_filename
            os.rename(orig, new)
            s.mugshot.name = new_filename
            s.save()
