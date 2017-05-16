from django.conf import settings
from django.contrib.auth.models import User

from djtools.utils.users import in_group

users = User.objects.filter( id__lte=10000)

print users.count()

count = 1

for u in users:
    if in_group(u, 'carthageFacultyStatus'):
        print '{}) {} | {}, {} | {}'.format(
            count, u.id, u.last_name, u.first_name, u.email
        )
        count += 1
