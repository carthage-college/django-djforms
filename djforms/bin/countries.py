from djforms.polisci.model_united_nations import COUNTRIES
from djforms.polisci.model_united_nations.models import Country

# delete all countries
Country.objects.all().delete()

# load new country set from tuple of tuples
for c in COUNTRIES:
    obj = Country(name=c[0])
    obj.save()
