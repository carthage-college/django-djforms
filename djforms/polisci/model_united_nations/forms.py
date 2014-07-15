# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.forms import USZipCodeField

from djforms.polisci.mun.models import Attender
from djforms.polisci.mun.models import Countries
#from djforms.polisci.mun import COUNTRIES
from djforms.core.models import STATE_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Order

DELEGATIONS = (
    ('', '----'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

COUNTRIES = Countries.objects.filter(status=True).order_by("name")

class AttenderForm(forms.ModelForm):
    """
    A form to collect registration data for the Model United Nations
    """
    first_name = forms.CharField(
        max_length=128, label="Faculty advisor first name"
    )
    last_name = forms.CharField(
        max_length=128
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES), required=True
    )
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(
        help_text="Format: XXX-XXX-XXXX"
    )
    number_of_del = forms.TypedChoiceField(
        choices=DELEGATIONS, label="Number of delegations"
    )
    delegation_1 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_2 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_3 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_4 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_5 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    comments = forms.CharField(
        label="Questions/Comments",
        help_text="""
            Feel free to list alternate countries in the space above
            (include your choice and delegation number)
        """,
        widget=forms.Textarea, required=False
    )

    class Meta:
        model = Attender
        exclude = (
            'country','order','second_name','previous_name','salutation'
        )

class OrderForm(forms.ModelForm):
    """
    Payment choices and total
    """
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect()
    )
    total = forms.CharField(
        max_length=7,
        label="Registration Fee"
    )

    class Meta:
        model = Order
        fields = ('total',)

COUNTRIES = (
("","-Select-"),
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
