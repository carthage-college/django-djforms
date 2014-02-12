#!/usr/bin/python

from djforms.scholars.models import Presentation

import os, uuid

prez = Presentation.objects.all()

root_path = "/data2/django_projects/djforms/assets/"
upload_dir = "files/scholars/posters/2013"

for p in prez:
    if p.poster_file:
        orig         = root_path + p.poster_file.name
        print "orig = %s" % orig
        fname = p.poster_file.name.split('/')[-1]
        new_filename = "%s/%s" % (upload_dir, fname)
        new          = root_path + new_filename
        print "new  %s" % new
        os.rename(orig, new)
        p.poster_file.name = new_filename
        p.save()
