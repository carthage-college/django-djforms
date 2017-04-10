from djforms.giving.models import DonationContact
from djtools.fields import TODAY
from django.conf import settings

start_date = settings.GIVING_DAY_START_DATE

donors = DonationContact.objects.filter(
    order__time_stamp__gte=start_date
).filter(order__status__in=['approved','manual'])

print donors.count()

count = 1

for d in donors:
    if '&' in d.first_name or ' and ' in d.first_name.lower():
        for o in d.order.all():
            order = o
        print '{}) {} | {}, {} | {}'.format(
            count, o.total,
            d.last_name, d.first_name, d.email
        )
        count += 1
