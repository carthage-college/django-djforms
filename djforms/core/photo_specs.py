# -*- coding: utf-8 -*-

from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeThumb(processors.Resize):
    """Define our thumbnail resize processor."""

    width = 100
    height = 75
    crop = True

class ResizeDisplay(processors.Resize):
    """Define a display size resize processor."""

    width = 600

class EnchanceThumb(processors.Adjustment):
    """Create an adjustment processor to enhance the image at small sizes."""

    contrast = 1.2
    sharpness = 1.1

class Thumbnail(ImageSpec):
    """Define our thumbnail spec."""

    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [ResizeThumb, EnchanceThumb]

class Display(ImageSpec):
    """Establish our display specification."""

    increment_count = True
    processors = [ResizeDisplay]
