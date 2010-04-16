from django.db import models
from django.forms import ModelForm
from djforms.core.models import GenericContact, GenericChoice
from django.contrib.localflavor.us.models import USStateField

#Lacrosse Golf Invite Generic Model
class LacrosseGolfInvite(GenericContact):
    
    address             = models.CharField("Address", max_length=255)
    city                = models.CharField("City", max_length=128)
    state               = USStateField()
    zip                 = models.CharField("Zip", max_length=10)
    phone               = models.CharField("Phone #", max_length=12, help_text="Format: XXX-XXX-XXXX")
    num_golf_and_dinner = models.IntegerField("Number attending Golf/Dinner ($90.00 per person)", max_length=10)
    num_dinner_only     = models.IntegerField("Number attending Dinner only ($30.00 per person)", max_length=20)
    amount_due          = models.IntegerField("TOTAL AMOUNT DUE (confirmation notice will be sent to you)", max_length=30)
    email_1             = models.EmailField("Email 1",null=True, blank=True)
    email_2             = models.EmailField("Email 2",null=True, blank=True)
    email_3             = models.EmailField("Email 3",null=True, blank=True)
    email_4             = models.EmailField("Email 4",null=True, blank=True)
    place               = models.BooleanField("Place me in a golfing foursome.", help_text="Check for yes.",default=False)
    attend              = models.BooleanField("I AM UNABLE TO ATTEND, however my contribution to Carthage Men's Lacrosse will be sent.",help_text="Check for yes.", default=False)
