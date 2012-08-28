from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djforms.core.models import STATE_CHOICES

DELEGATIONS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class ModelUnitedNationsRegistrationForm(forms.Form):
    """
    A form to collect registration data for the Model United Nations
    """
    school_name         = forms.CharField(max_length=100, label="School name")
    faculty_advisor     = forms.CharField(max_length=100, label="Faculty advisor")
    school_address1     = forms.CharField(max_length=100, label="School address")
    school_address2     = forms.CharField(max_length=100, label="", required=False)
    city                = forms.CharField(max_length=100)
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code         = USZipCodeField(label="Zip Code")
    office              = forms.CharField(max_length=100)
    work_phone          = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    home_phone          = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX", required=False)
    email               = forms.EmailField()
    number_of_del       = forms.TypedChoiceField(choices=DELEGATIONS, label="Number of delegations")
    number_of_stu       = forms.CharField(max_length=3, label="Number of students")
    comments            = forms.CharField(label="Questions/Comments", help_text="Feel free to list alternate countries in the space below (include your choice and delegation number)", widget=forms.Textarea, required=False)

COUNTRIES = (
("","Choose a country..."),
("Afghanistan","Afghanistan"),
("Algeria","Algeria"),
("Argentina","Argentina"),
("Azerbaijan*","Azerbaijan*"),
("Belarus","Belarus"),
("Bosnia and Herzegovina","Bosnia-Herzegovina"),
("Botswana","Botswana"),
("Brazil","Brazil"),
("Bulgaria","Bulgaria"),
("Burkino Faso","Burkino Faso"),
("Cambodia","Cambodia"),
("Canada","Canada"),
("Chile","Chile"),
("China*","China*"),
("Colombia*","Colombia*"),
("Costa Rica","Costa Rica"),
("Cuba","Cuba"),
("Dominican Republic","Dominican Republic"),
("Ecuador","Ecuador"),
("Egypt","Egypt"),
("Ethiopia","Ethiopia"),
("France*","France*"),
("Gabon","Gabon"),
("Germany*","Germany*"),
("Ghana","Ghana"),
("Greece*","Greece*"),
("Guatemala*","Guatemala*"),
("Haiti","Haiti"),
("Honduras","Honduras"),
("India*","India*"),
("Indonesia","Indonesia"),
("Iran","Iran"),
("Iraq","Iraq"),
("Israel","Israel"),
("Italy","Italy"),
("Japan","Japan"),
("Jordan","Jordan"),
("Kenya","Kenya"),
("Laos","Laos"),
("Lebanon","Lebanon"),
("Libya","Libya"),
("Mexico","Mexico"),
("Morocco*","Morocco*"),
("Mozambique","Mozambique"),
("New Zealand","New Zealand"),
("Nicaragua","Nicaragua"),
("Nigeria","Nigeria"),
("North Korea","North Korea"),
("Oman","Oman"),
("Pakistan*","Pakistan*"),
("Paraguay","Paraguay"),
("Philippines","Philippines"),
("Portugal*","Portugal*"),
("Romania","Romania"),
("Russia*","Russia*"),
("Rwanda*","Rwanda*"),
("Saudi Arabia","Saudi Arabia"),
("Somalia","Somalia"),
("South Africa*","South Africa*"),
("South Korea","South Korea"),
("Spain*","Spain*"),
("Sudan*","Sudan*"),
("Sweden","Sweden"),
("Switzerland","Switzwerland"),
("Syria","Syria"),
("Thailand","Thailand"),
("Timor-Leste","Timor-Leste"),
("Togo*","Togo*"),
("Turkey","Turkey"),
("Uganda","Uganda"),
("Ukraine","Ukraine"),
("United Kingdom*","United Kingdom*"),
("United States*","United States*"),
("Uzbekistan","Uzbekistan"),
("Venezuela","Venezuela"),
("Vietnam","Vietnam"),
("Yemen","Yemen"),
("Zambia","Zambia"),
("Zimbabwe","Zimbabwe")
)

class ModelUnitedNationsCountriesForm(forms.Form):
    # delegation 1
    d1c1  = forms.TypedChoiceField(choices=COUNTRIES)
    d1c2  = forms.TypedChoiceField(choices=COUNTRIES)
    d1c3  = forms.TypedChoiceField(choices=COUNTRIES)
    d1c4  = forms.TypedChoiceField(choices=COUNTRIES)
    d1c5  = forms.TypedChoiceField(choices=COUNTRIES)
    # delegation 2
    d2c1  = forms.TypedChoiceField(choices=COUNTRIES)
    d2c2  = forms.TypedChoiceField(choices=COUNTRIES)
    d2c3  = forms.TypedChoiceField(choices=COUNTRIES)
    d2c4  = forms.TypedChoiceField(choices=COUNTRIES)
    d2c5  = forms.TypedChoiceField(choices=COUNTRIES)
    # delegation 3
    d3c1  = forms.TypedChoiceField(choices=COUNTRIES)
    d3c2  = forms.TypedChoiceField(choices=COUNTRIES)
    d3c3  = forms.TypedChoiceField(choices=COUNTRIES)
    d3c4  = forms.TypedChoiceField(choices=COUNTRIES)
    d3c5  = forms.TypedChoiceField(choices=COUNTRIES)
    # delegation 4
    d4c1  = forms.TypedChoiceField(choices=COUNTRIES)
    d4c2  = forms.TypedChoiceField(choices=COUNTRIES)
    d4c3  = forms.TypedChoiceField(choices=COUNTRIES)
    d4c4  = forms.TypedChoiceField(choices=COUNTRIES)
    d4c5  = forms.TypedChoiceField(choices=COUNTRIES)
    # delegation 5
    d5c1  = forms.TypedChoiceField(choices=COUNTRIES)
    d5c2  = forms.TypedChoiceField(choices=COUNTRIES)
    d5c3  = forms.TypedChoiceField(choices=COUNTRIES)
    d5c4  = forms.TypedChoiceField(choices=COUNTRIES)
    d5c5  = forms.TypedChoiceField(choices=COUNTRIES)
