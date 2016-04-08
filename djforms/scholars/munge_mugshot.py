#!/usr/bin/python

#
# don't forget to chown -R the files/scholars directory
#

from django.conf import settings

from djforms.scholars.models import Presentation

import os, uuid

from djtools.fields import TODAY

YEAR = int(TODAY.year)

prez = Presentation.objects.filter(date_updated__year=YEAR)

root_path = os.path.join(settings.ROOT_DIR, "assets")
upload_dir = "files/scholars/mugshots/"
count = 1

for p in prez:
    for s in p.presenters.all():
        if s.mugshot:
            orig = os.path.join(root_path, s.mugshot.name)
            new_filename = "{}{}_{}_{}.jpg".format(
                upload_dir, s.last_name, s.first_name, uuid.uuid4().hex
            )
            new = os.path.join(root_path, new_filename)
            print "{}) {} {} ".format(
                count, s.mugshot.name, new_filename
            )
            count += 1
            try:
                os.rename(orig, new)
                s.mugshot.name = new_filename
                s.save()
            except:
                print "No such file or directory or permissions problem"
                print "Original: {}".format(orig)
                print "New: {}".format(new)

