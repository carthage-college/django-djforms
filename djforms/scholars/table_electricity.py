#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import django
import os
import sys
import uuid


# primt django
django.setup()
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djforms.settings.shell')


from django.conf import settings
from djforms.scholars.models import Presentation


# set up command-line options
desc = """
    Accepts as input the year to munge
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-y',
    '--year',
    required=True,
    help="Year to munge.",
    dest='year',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Display presentations that need a table or electricty."""
    presentations = Presentation.objects.filter(date_created__year=year)
    for prez in presentations:
        if prez.need_table == 'Yes' or prez.need_electricity == 'Yes':
            print(
                '{0}|{1}|{2}'.format(
                    prez.need_table, prez.need_electricity, prez.user.email,
                ),
            )


if __name__ == '__main__':
    args = parser.parse_args()
    year = args.year
    test = args.test
    sys.exit(main())
