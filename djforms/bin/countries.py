from djforms.polisci.model_united_nations import COUNTRIES
from djforms.polisci.model_united_nations.models import Country

for c in COUNTRIES:
    obj = Country(name=c[0])
    obj.save()
