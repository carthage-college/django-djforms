# -*- coding: utf-8 -*-
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
    comments            = forms.CharField(label="Questions/Comments", help_text="Feel free to list alternate countries in the space above (include your choice and delegation number)", widget=forms.Textarea, required=False)

COUNTRIES = (
("","Choose a country..."),
("Afghanistan","Afghanistan"),
("Albania","Albania"),
("Algeria*","Algeria*"),
("Andorra","Andorra"),
("Angola","Angola"),
("Antigua and Barbuda","Antigua and Barbuda"),
("Argentina^","Argentina^"),
("Armenia","Armenia"),
("Australia^","Australia^"),
("Austria","Austria"),
("Azerbaijan~","Azerbaijan~"),
("Bahamas","Bahamas"),
("Bahrain","Bahrain"),
("Bangladesh","Bangladesh"),
("Barbados","Barbados"),
("Belarus","Belarus"),
("Belgium*","Belgium*"),
("Belize","Belize"),
("Benin","Benin"),
("Bhutan","Bhutan"),
("Bolivia","Bolivia"),
("Bosnia and Herzegovina","Bosnia and Herzegovina"),
("Botswana","Botswana"),
("Brazil*","Brazil*"),
("Brunei Darussalam","Brunei Darussalam"),
("Bulgariai*","Bulgaria*"),
("Burkino Faso","Burkino Faso"),
("Burundi","Burundi"),
("Cambodia","Cambodia"),
("Cameroon","Cameroon"),
("Canada*","Canada*"),
("Cape Verde","Cape Verde"),
("Central African Republic","Central African Republic"),
("Chad","Chad"),
("Chile","Chile"),
("China^","China^"),
("Colombia","Colombia"),
("Comoros","Comoros"),
("Republic of Congo","Republic of Congo"),
("Democratic Republic of the Congo","Democratic Republic of the Congo"),
("Costa Rica*","Costa Rica*"),
("Côte d'Ivoire","Côte d'Ivoire"),
("Croatia","Croatia"),
("Cuba*","Cuba*"),
("Cyprus","Cyprus"),
("Czech Republic","Czech Republic"),
("Denmark","Denmark"),
("Djibouti","Djibouti"),
("Dominica","Dominic"),
("Dominican Republic","Dominican Republic"),
("Ecuador","Ecuador"),
("Egypt*","Egypt*"),
("El Salvador","El Salvador"),
("Equatorial Guinea","Equatorial Guinea"),
("Eritrea","Eritrea"),
("Estonia","Estonia"),
("Ethiopia","Ethiopia"),
("Fiji","Fiji"),
("Finland","Finland"),
("France^","France^"),
("Gabon","Gabon"),
("Gambia","Gambia"),
("Georgia","Georgia"),
("Germany*","Germany*"),
("Ghana","Ghana"),
("Greece*","Greece*"),
("Grenada","Grenada"),
("Guatemala~","Guatemala~"),
("Guinea","Guinea"),
("Guinea-Bissau","Guinea-Bissau"),
("Guyana","Guyana"),
("Haiti","Haiti"),
("Honduras","Honduras"),
("Hungary*","Hungary*"),
("Iceland","Iceland"),
("India*","India*"),
("Indonesia*","Indonesia*"),
("Iran","Iran"),
("Iraq","Iraq"),
("Ireland","Ireland"),
("Israel","Israel"),
("Italy*","Italy*"),
("Jamaica","Jamaica"),
("Japan*","Japan*"),
("Jordan","Jordan"),
("Kazakhstan","Kazakhstan"),
("Kenya","Kenya"),
("Kiribati","Kiribati"),
("Democratic People's Republic of Korea","Democratic People's Republic of Korea"),
("Republic of Korea^","Republic of Korea^"),
("Kuwait","Kuwait"),
("Kyrgyzstan","Kyrgyzstan"),
("Lao People's Democratic Republic","Lao People's Democratic Republic"),
("Latvia","Latvia"),
("Lebanon","Lebanon"),
("Lesotho","Lesotho"),
("Liberia","Liberia"),
("Libya*","Libya*"),
("Liechtenstein","Liechtenstein"),
("Lithuania","Lithuania"),
("Luxembourg~","Luxembourg~"),
("Macedonia","Macedonia"),
("Madagascar","Madagascar"),
("Malawi","Malawi"),
("Malaysia","Malaysia"),
("Maldives","Maldives"),
("Mali","Mali"),
("Malta","Malta"),
("Marshall Islands","Marshall Islands"),
("Mauritania","Mauritania"),
("Mauritius","Mauritius"),
("Mexico*","Mexico*"),
("Micronesia (Federated States of)","Micronesia (Federated States of)"),
("Republic of Moldova","Republic of Moldova"),
("Monaco","Monaco"),
("Mongolia","Mongolia"),
("Montenegro","Montenegro"),
("Morocco~","Morocco~"),
("Mozambique","Mozambique"),
("Myanmar (Burma)","Myanmar (Burma)"),
("Namibia","Namibia"),
("Nauru","Nauru"),
("Nepal","Nepal"),
("Netherlands","Netherlands"),
("New Zealand","New Zealand"),
("Nicaragua","Nicaragua"),
("Niger","Niger"),
("Nigeria*","Nigeria*"),
("Norway*","Norway*"),
("Oman","Oman"),
("Pakistan^","Pakistan^"),
("Palau","Palau"),
("Panama","Panama"),
("Papua New Guinea","Papua New Guinea"),
("Paraguay","Paraguay"),
("Peru","Peru"),
("Philippines","Philippines"),
("Poland*","Poland*"),
("Portugal","Portugal"),
("Qatar","Qatar"),
("Romania","Romania"),
("Russian Federation^","Russia Federation^"),
("Rwanda~","Rwanda~"),
("Saint Kitts and Nevis","Saint Kitts and Nevis"),
("Saint Lucia","Saint Lucia"),
("Saint Vincent and the Grenadines","Saint Vincent and the Grenadines"),
("Samoa","Samoa"),
("San Marino","San Marino"),
("Sao Tome and Principe","Sao Tome and Principe"),
("Saudi Arabia*","Saudi Arabia*"),
("Senegal","Senegal"),
("Serbia","Serbia"),
("Seychelles","Seychelles"),
("Sierra Leone","Sierra Leone"),
("Singapore","Singapore"),
("Slovakia","Slovakia"),
("Slovenia","Slovenia"),
("Solomon Islands","Solomon Islands"),
("Somalia","Somalia"),
("South Africa*","South Africa*"),
("South Sudan","South Sudan"),
("Spain","Spain"),
("Sri Lanka","Sri Lanka"),
("Sudan","Sudan"),
("Suriname","Suriname"),
("Swaziland","Swaziland"),
("Sweden*","Sweden*"),
("Switzerland","Switzwerland"),
("Syrian Arab Republic","Syrian Arab Republic"),
("Tajikistan","Tajikistan"),
("Tanzania*","Tanzania*"),
("Thailand*","Thailand*"),
("Timor-Leste","Timor-Leste"),
("Togo~","Togo~"),
("Tonga","Tonga"),
("Trinidad and Tobago","Trinidad and Tobago"),
("Tunisia","Tunisia"),
("Turkey","Turkey"),
("Turkmenistan","Turkmenistan"),
("Tuvalu","Tuvalu"),
("Uganda","Uganda"),
("Ukraine","Ukraine"),
("United Arab Emirates","United Arab Emirates"),
("United Kingdom^","United Kingdom^"),
("United States^","United States^"),
("Uruguay*","Uruguay*"),
("Uzbekistan","Uzbekistan"),
("Vanuatu","Vanuatu"),
("Venezuela","Venezuela"),
("Viet Nam","Viet Nam"),
("Yemen","Yemen"),
("Zambia","Zambia"),
("Zimbabwe","Zimbabwe"),
)

class ModelUnitedNationsCountriesForm(forms.Form):
    # delegation 1
    d1c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 2
    d2c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 3
    d3c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 4
    d4c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 5
    d5c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
