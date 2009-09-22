# -*- coding: utf-8 -*-

import logging
from django.conf import settings

logging.basicConfig(format='%(name)s [%(funcName)s]: %(message)s')

if settings.DEBUG:
    for name in ['views', 'models']:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
