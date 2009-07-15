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
ROOM_CHOICES=[  ('', '---------- pick one ----------'),
                ('Hedberg Library 105','Hedberg Library 105'),
                ('Hedberg Library 106','Hedberg Library 106'),
                ('Hedberg Library 107','Hedberg Library 107'),
                ('Hedberg Library 108','Hedberg Library 108'),
                ('Hedberg Library 109','Hedberg Library 109'),
                ('Hedberg Library 159','Hedberg Library 159'),
                ('Hedberg Library 162','Hedberg Library 162'),
                ('Hedberg Library 163','Hedberg Library 163'),
                ('Hedberg Library 164','Hedberg Library 164'),
                ('Hedberg Library 170','Hedberg Library 170'),
                ('Hedberg Library 172','Hedberg Library 172'),
                ('Hedberg Library 217','Hedberg Library 217'),
                ('Johnson Art Center 103','Johnson Art Center 103'),
                ('Johnson Art Center 117','Johnson Art Center 117'),
                ('Johnson Art Center 140','Johnson Art Center 140'),
                ('Johnson Art Center 142','Johnson Art Center 142'),
                ('Johnson Art Center 205','Johnson Art Center 205'),
                ('Johnson Art Center 207','Johnson Art Center 207'),
                ('Johnson Art Center 209','Johnson Art Center 209'),
                ('Johnson Art Center 215','Johnson Art Center 215'),
                ('Johnson Art Center 216','Johnson Art Center 216'),
                ('Johnson Art Center 219','Johnson Art Center 219'),
                ('Johnson Art Center 252','Johnson Art Center 252'),
                ('Johnson Art Center 253','Johnson Art Center 253'),
                ('Lentz Hall 200','Lentz Hall 200'),
                ('Lentz Hall 201','Lentz Hall 201'),
                ('Lentz Hall 202','Lentz Hall 202'),
                ('Lentz Hall 203','Lentz Hall 203'),
                ('Lentz Hall 220','Lentz Hall 220'),
                ('Lentz Hall 221','Lentz Hall 221'),
                ('Lentz Hall 222','Lentz Hall 222'),
                ('Lentz Hall 223','Lentz Hall 223'),
                ('Lentz Hall 224','Lentz Hall 224'),
                ('Lentz Hall 225','Lentz Hall 225'),
                ('Lentz Hall 227','Lentz Hall 227'),
                ('Lentz Hall 229','Lentz Hall 229'),
                ('Lentz Hall 230','Lentz Hall 230'),
                ('Lentz Hall 231','Lentz Hall 231'),
                ('Lentz Hall 233','Lentz Hall 233'),
                ('Lentz Hall 234','Lentz Hall 234'),
                ('Lentz Hall 300','Lentz Hall 300'),
                ('Lentz Hall 318','Lentz Hall 318'),
                ('Lentz Hall 319','Lentz Hall 319'),
                ('Lentz Hall 332','Lentz Hall 332'),
                ('Lentz Hall 337','Lentz Hall 337'),
                ('Lentz Hall 424','Lentz Hall 424'),
                ('Lentz Hall 425','Lentz Hall 425'),
                ('Lentz Hall 426','Lentz Hall 426'),
                ('Lentz Hall 432','Lentz Hall 432'),
                ('Lentz Hall Ahrens','Lentz Hall Ahrens'),
                ('Straz 106','Straz 106'),
                ('Straz 107','Straz 107'),
                ('Straz 109','Straz 109'),
                ('Straz 110','Straz 110'),
                ('Straz 111','Straz 111'),
                ('Straz 117','Straz 117'),
                ('Straz 119','Straz 119'),
                ('Straz 123','Straz 123'),
                ('Straz 125','Straz 125'),
                ('Straz 129','Straz 129'),
                ('Straz 210','Straz 210'),
                ('Straz 215','Straz 215'),
                ('Straz 218','Straz 218'),
                ('Straz 220','Straz 220'),
                ('Straz 223','Straz 223'),
                ('Straz 227','Straz 227'),
                ('Straz 233','Straz 233'),
                ('Straz B 4','Straz B 4'),
                ('Straz B12','Straz B12'),]
class RoomReserveForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(label='Your e-mail')
    local_phone = forms.CharField(max_length=20)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    date = forms.DateField(widget=DateTimeWidget)
    start_time_hours = forms.ChoiceField(choices=HOUR_CHOICES)
    start_time_minutes = forms.ChoiceField(choices=MINUTE_CHOICES)
    start_time_meridiem = forms.ChoiceField(choices=MERIDIEM_CHOICES)
    start_time = forms.TimeField(required=False)
    end_time_hours = forms.ChoiceField(choices=HOUR_CHOICES)
    end_time_minutes = forms.ChoiceField(choices=MINUTE_CHOICES)
    end_time_meridiem = forms.ChoiceField(choices=MERIDIEM_CHOICES)
    end_time = forms.TimeField(required=False)
    room = forms.ChoiceField(ROOM_CHOICES)
    title_of_event = forms.CharField(required=False, max_length=50)
    department = forms.CharField(required=False, max_length=50)
    course_number = forms.CharField(required=False, max_length=25)
    additional_requests = forms.CharField(required=False, widget=forms.Textarea)
    comments = forms.CharField(required=False, widget=forms.Textarea)

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
    
    def clean_start_time(self):
        #assign proper data
        start_time = self.cleaned_data['start_time']
        start_time_meridiem = self.cleaned_data['start_time_meridiem']
        start_time_hours = int(self.cleaned_data['start_time_hours'])
        start_time_minutes = int(self.cleaned_data['start_time_minutes'])
        #convert the time to seconds
        start_time = ( start_time_hours * 3600 ) + ( start_time_minutes * 60 )
        return start_time
        
    def clean_end_time(self):
        #assign proper data, we need start time stuff for validation comparison
        start_time = self.cleaned_data['start_time']
        start_time_meridiem = self.cleaned_data['start_time_meridiem']
        start_time_hours = int(self.cleaned_data['start_time_hours'])
        end_time = self.cleaned_data['end_time']
        end_time_meridiem = self.cleaned_data['end_time_meridiem']
        end_time_hours = int(self.cleaned_data['end_time_hours'])
        end_time_minutes = int(self.cleaned_data['end_time_minutes'])
        #set the time to the proper amount of seconds
        end_time = (end_time_hours * 3600) + ( end_time_minutes * 60 )
        end_time2 = end_time
        #compare the two based on seconds and meridiem
        if start_time_meridiem == 'p.m.' and end_time_meridiem == 'a.m.':
            raise forms.ValidationError("Your end time must remain in the same day as your start time!")
        if start_time_meridiem == end_time_meridiem:
            if start_time_hours == 12:
                start_time = start_time - 43200
            if end_time_hours == 12:
                end_time2 = end_time2 - 43200
            if end_time2 <= start_time:
                raise forms.ValidationError("Your end time must come after your start time!")
        return end_time
