from djforms.lis.conferences.course_ference.models import CourseFerenceAttender

from json import dumps
from pygeocoder import Geocoder

import sys

def main():
    count=1
    cfa = CourseFerenceAttender.objects.filter(postal_code__isnull=False)
    for c in cfa:
        address = "%s, %s, %s %s, USA" % (c.address1, c.city, c.state, c.postal_code)
        results = Geocoder.geocode(address)
        print(address)
        print(results[0].coordinates)
        print(results[0])
        count += 1

if __name__ == "__main__":
    sys.exit(main())

