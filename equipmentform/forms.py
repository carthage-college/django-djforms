from django import forms
from djforms.widgets import *
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
                    ('Camcorder', 'Camcorder *'),
                    ('CDM Camcorder', 'CDM Camcorder **'),
                    ('Tripod', 'Tripod'),
                    ('Microphone', 'Microphone'),
                    ('Slide projector', 'Slide projector'),]
HOUR_CHOICES=[  (12, '12'),
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
                (6, '6'),
                (7, '7'),
                (8, '8'),
                (9, '9'),
                (10, '10'),
                (11, '11'),]
MINUTE_CHOICES=[(0, '00'),
                (5, '05'),
                (10, '10'),
                (15, '15'),
                (20, '20'),
                (25, '25'),
                (30, '30'),
                (35, '35'),
                (40, '40'),
                (45, '45'),
                (50, '50'),
                (55, '55'),]
MERIDIEM_CHOICES=[  ('p.m.','p.m.'),
                    ('a.m.','a.m.'),]
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
    date = forms.DateField(widget=DateTimeWidget)
    start_time_hours = forms.ChoiceField(choices=HOUR_CHOICES)
    start_time_minutes = forms.ChoiceField(choices=MINUTE_CHOICES)
    start_time_meridiem = forms.ChoiceField(choices=MERIDIEM_CHOICES)
    start_time = forms.TimeField(required=False)
    end_time_meridiem = forms.ChoiceField(choices=MERIDIEM_CHOICES, required=False)
    end_time = forms.TimeField(required=False)
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
    
    #Time is set to its hours and minutes values, the meridiem is what determines the time later on
    def clean_start_time(self):
        #assign proper data
        start_time = self.cleaned_data['start_time']
        start_time_meridiem = self.cleaned_data['start_time_meridiem']
        start_time_hours = int(self.cleaned_data['start_time_hours'])
        start_time_minutes = int(self.cleaned_data['start_time_minutes'])
        #convert the time to seconds
        start_time = ( start_time_hours * 3600 ) + ( start_time_minutes * 60 )
        return start_time
    
    
