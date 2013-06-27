from djforms.lis.conferences.course_ference.models import CourseFerenceAttender

from json import dumps
from pygeocoder import Geocoder

import sys

def main():
    cfa = CourseFerenceAttender.objects.filter(postal_code__isnull=False)
    for c in cfa:
        #c.country="US"
        #c.latitude  = None
        #c.longitude = None
        #c.save()
        if not c.latitude and not c.longitude:
            address = "%s, %s, %s %s, %s" % (c.address1, c.city, c.state, c.postal_code, c.country)
            results = Geocoder.geocode(address)
            print address
            # format is (long, lat)
            coords = results[0].coordinates
            print coords
            c.longitude = str(coords[0])
            c.latitude  = str(coords[1])
            c.save()

if __name__ == "__main__":
    sys.exit(main())

