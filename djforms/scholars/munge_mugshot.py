#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#
# don't forget to chown -R the files/scholars directory
#

import os
import uuid
import django


django.setup()


from django.conf import settings
from djforms.scholars.models import Presentation
from djtools.fields import TODAY


YEAR = int(TODAY.year)
presentations = Presentation.objects.filter(date_updated__year=YEAR)
root_path = os.path.join(settings.ROOT_DIR, "assets")
upload_dir = "files/scholars/mugshots/"
count = 1

for prez in presentations:
    for presenter in prez.presenters.all():
        if presenter.mugshot:
            orig = os.path.join(root_path, presenter.mugshot.name)
            new_filename = "{0}{1}_{2}_{3}.jpg".format(
                upload_dir,
                presenter.last_name,
                presenter.first_name,
                uuid.uuid4().hex,
            )
            new = os.path.join(root_path, new_filename)
            print('{0}) {1} {2} '.format(count, presenter.mugshot.name, new_filename))
            count += 1
            try:
                os.rename(orig, new)
                presenter.mugshot.name = new_filename
                presenter.save()
            except Exception:
                print("No such file or directory or permissions problem.")
                print("Original: {0}".format(orig))
                print("New: {1}".format(new))
