from django import forms
from django.contrib import admin
from djforms.alumni.classnotes.models import Contact
from djforms.alumni.classnotes.forms import CLASSYEARS, SPOUSEYEARS

class ContactAdminForm(forms.ModelForm):
    classyear       = forms.CharField(label="Class", max_length=4, widget=forms.Select(choices=CLASSYEARS))
    spouseyear      = forms.CharField(label="Spouse's class", max_length=4, widget=forms.Select(choices=SPOUSEYEARS), required=False)
    email           = forms.EmailField(label="Email", required=False)

    class Meta(object):
        model = Contact

    def __init__(self,*args,**kwargs):
        super(ContactAdminForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = ['salutation','first_name','last_name','second_name',
                                'suffix','previous_name','email','classyear','spousename',
                                'spousemaidenname','spouseyear','classnote','alumnicomments',
                                'pubstatus','pubstatusdate','carthaginianstatus','alumnistatus',
                                'picture','caption']

class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm
    ordering = ('last_name','name','previous_name','classyear','alumnistatus','pubstatus','carthaginianstatus')
    list_display = ('last_name','first_name','salutation','name','previous_name','suffix','classyear','created_at','alumnistatus','pubstatus','carthaginianstatus')
    search_fields = ('last_name','name','previous_name','classyear')

admin.site.register(Contact,ContactAdmin)

