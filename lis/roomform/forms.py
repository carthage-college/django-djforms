from django import forms
from djforms.core.fields import KungfuTimeField

STATUS_CHOICES=[('', '---------- select ----------'),
                ('Trustee', 'Trustee'),
                ('Administration', 'Administration'),
                ('Faculty', 'Faculty'),
                ('Adjunct Faculty', 'Adjunct Faculty'),
                ('TLE', 'TLE'),
                ('Staff', 'Staff'),
                ('Graduate Student', 'Graduate Student'),
                ('Undergraduate Student', 'Undergraduate Student'),]
ROOM_CHOICES=[  ('', '---------- pick one ----------'),
                ('Clausen Center 105','Clausen Center 105'),
                ('Clausen Center 106','Clausen Center 106'),
                ('Clausen Center 107','Clausen Center 107'),
                ('Clausen Center 108','Clausen Center 108'),
                ('Clausen Center 111','Clausen Center 111'),
                ('Clausen Center 112','Clausen Center 112'),
                ('Clausen Center 113','Clausen Center 113'),
                ('Clausen Center 114','Clausen Center 114'),
                ('Clausen Center 117','Clausen Center 117'),
                ('Clausen Center 204','Clausen Center 204'),
                ('Clausen Center 205','Clausen Center 205'),
                ('Clausen Center 206','Clausen Center 206'),
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
    date = forms.DateField()
    start_time = KungfuTimeField()
    end_time = KungfuTimeField()
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
        if date < datetime.date.today():
            raise forms.ValidationError("You must pick a date after today!")
        return date
