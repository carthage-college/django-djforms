from djforms.lis.conferences.course_ference.models import CourseFerenceAttender

from json import dumps

cfa = CourseFerenceAttender.objects.filter(postal_code__isnull=False)

jay = "["

for c in cfa:
    # json encode
    jay += '{"lat":"","long":"","creator":"Carthage College","created":1310499032,'
    jay += '"name":"%s",' % c.affiliation
    jay += '"address":"%s, %s, %s %s, USA"},' % (c.address1, c.city, c.state, c.postal_code)
jay = jay[:-1] + "]"

print jay
