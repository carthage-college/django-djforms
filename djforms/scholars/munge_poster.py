# -*- coding: utf-8 -*-
#!/usr/bin/env

import os
import sys
import uuid
import argparse

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_current/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djforms.settings')

# primt django
import django
django.setup()

from django.conf import settings

from djforms.scholars.models import Presentation

# set up command-line options
desc = """
Accepts as input the year to munge
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-y', '--year',
    required=True,
    help="Year to munge.",
    dest='year'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)


def main():

    prez = Presentation.objects.filter(date_created__year=year)

    root_path = settings.MEDIA_ROOT
    upload_dir = '/files/scholars/posters/{}/'.format(year)

    for p in prez:
        if p.poster_file:
            # original file
            orig = '{}/{}'.format(root_path, p.poster_file.name)
            # new file
            fname = p.poster_file.name.split('/')[-1]
            new_filename = '{}{}'.format(upload_dir, fname)
            new = root_path + new_filename
            # rename and save
            if not test:
                os.rename(orig, new)
                p.poster_file.name = new_filename
                p.save()
            else:
                #print "orig = {}".format(orig)
                print orig
                #print "new  {}".format(new)


######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    year = args.year
    test = args.test

    sys.exit(main())
