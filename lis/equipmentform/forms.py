from django import forms
from djtools.fields.time import KungfuTimeField

import datetime

STATUS_CHOICES=[('', '---------- pick one ----------'),
                ('Trustee', 'Trustee'),
                ('Administration', 'Administration'),
                ('Faculty', 'Faculty'),
                ('Adjunct Faculty', 'Adjunct Faculty'),
                ('TLE', 'TLE'),
                ('Staff', 'Staff'),
                ('Graduate Student', 'Graduate Student'),
                ('Undergraduate Student', 'Undergraduate Student'),]
EQUIPMENT_CHOICES=[ ('MacBook', 'MacBook'),
                    ('MacBook Pro', 'MacBook Pro'),
                    ('PC laptop', 'PC laptop'),
                    ('Data Projector', 'Data Projector'),
                    ('Digital Camera', 'Digital Camera (for still photos)*'),
                    ('Document Camera', 'Document Camera'),
                    ('Camcorder', 'Camcorder *'),
                    ('Flip Camcorder', 'Flip Camcorder'),
                    ('CDM Camcorder', 'CDM Camcorder **'),
                    ('Voice Recorder', 'Voice Recorder'),
                    ('Microphone', 'Microphone'),
                    ('Tripod', 'Tripod'),
                    ('Projection Screen', 'Projection Screen'),
                    ('Slide projector', 'Slide projector'),]

class EquipmentReserveForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(label='Your e-mail')
    local_phone = forms.CharField(max_length=20)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    title_of_event = forms.CharField(required=False, max_length=50)
    department = forms.CharField(required=False, max_length=50)
    course_number = forms.CharField(required=False, max_length=25)
    equipment = forms.MultipleChoiceField(choices=EQUIPMENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    date = forms.DateField()
    start_time = KungfuTimeField()
    end_time = KungfuTimeField()

    #Makes sure the user enters a first name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == 'Enter first name':
            raise forms.ValidationError("Enter a First Name!")
        return first_name

    #Makes sure the user enters a last name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name == 'Enter last name':
            raise forms.ValidationError("Enter a Last Name!")
        return last_name

    #Makes sure the user enters a phone number
    def clean_local_phone(self):
        local_phone = self.cleaned_data['local_phone']
        if local_phone == 'Enter phone number':
            raise forms.ValidationError("Enter a Phone Number!")
        return local_phone

    #Makes sure the user picks a date later than today
    def clean_date(self):
        date = self.cleaned_data['date']
        if date <= datetime.date.today():
            raise forms.ValidationError("You must pick a date after today!")
        return date

    #Makes sure the user picks an end time after the start time    
    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data['start_time']
        if end_time <= start_time:
            raise forms.ValidationError("End time must be after start time!")
        return end_time
