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
                                'spousepreviousname','spouseyear','classnote','alumnicomments',
                                'pubstatus','pubstatusdate','carthaginianstatus','alumnistatus',
                                'picture','caption']

class ContactAdmin(admin.ModelAdmin):
    form            = ContactAdminForm
    ordering        = ('last_name','classyear','alumnistatus','pubstatus','carthaginianstatus')
    list_display    = ('last_name','first_name','classyear','created_at','alumnistatus','pubstatus','carthaginianstatus')
    search_fields   = ('last_name','first_name','previous_name','classyear')
    list_filter     = ('alumnistatus','pubstatus','carthaginianstatus')

    actions = ['set_carthiginian_status']

    def set_carthiginian_status(self, request, queryset):
        """
        Loop through all contacts and set carthaginian status
        """
        for obj in queryset:
            obj.carthaginianstatus=True
            obj.save()

        self.message_user(request, '%s alumni notes were successfully updated to "published in Carthaginian".' % len(queryset))

    set_carthiginian_statusshort_description = 'Update Carthaginian status'

admin.site.register(Contact,ContactAdmin)

