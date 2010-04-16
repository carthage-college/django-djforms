from django import forms
from djforms.lacrossegolfinvite.models import *
from tagging.models import Tag, TaggedItem
#from djforms.core.models import STATE_CHOICES
from django.contrib.localflavor.us.forms import USPhoneNumberField
                                        
class LacrosseGolfInviteForm(forms.ModelForm):
    #state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    phone      = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    place_str  = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    attend_str = forms.CharField(required=False, max_length=5, widget=forms.HiddenInput())
    
    class Meta:
        model = LacrosseGolfInvite
        
    def clean_place_str(self):
        temp_place = 'No'
        cur_place = self.cleaned_data['place']
        if cur_place == True:
            temp_place = 'Yes'
        return temp_place
        
    def clean_attend_str(self):
        temp_attend = 'No'
        cur_attend = self.cleaned_data['attend']
        if cur_attend == False:
            temp_attend = 'Yes'
        return temp_attend
        
    def clean_amount_due(self):
        golf_and_dinner_num = self.cleaned_data['num_golf_and_dinner']
        only_dinner_num = self.cleaned_data['num_dinner_only']
        calc_total = (90 * golf_and_dinner_num) + (30 * only_dinner_num)
        return calc_total
