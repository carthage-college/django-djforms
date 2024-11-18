# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.contrib import admin
from djforms.alumni.classnotes.models import Contact
from djforms.alumni.classnotes.forms import CLASSYEARS, SPOUSEYEARS, CATEGORIES
from djtools.utils.mail import send_mail
from image_cropping import ImageCroppingMixin


class ContactAdminForm(forms.ModelForm):
    classyear       = forms.CharField(label="Class", max_length=4, widget=forms.Select(choices=CLASSYEARS))
    spouseyear      = forms.CharField(label="Spouse's class", max_length=4, widget=forms.Select(choices=SPOUSEYEARS), required=False)
    email           = forms.EmailField(label="Email", required=False)
    category        = forms.CharField(label="Category", widget=forms.Select(choices=CATEGORIES), required=True)

    class Meta(object):
        model = Contact
        fields = '__all__'


class ContactAdmin(ImageCroppingMixin, admin.ModelAdmin):
    form            = ContactAdminForm
    ordering        = ('-created_at', 'last_name','classyear','alumnistatus','pubstatus','carthaginianstatus','category')
    list_display    = ('last_name','first_name','classyear','created_at','alumnistatus','pubstatus','carthaginianstatus','category','admin_image')
    search_fields   = ('last_name','first_name','previous_name','classyear')
    list_filter     = ('alumnistatus','pubstatus','carthaginianstatus','category')

    fieldsets = (
        ('Name, Class, Email', {
            'fields': ('salutation','first_name','last_name','second_name','suffix','previous_name','classyear','email','hometown')
        }),
        ('Spouse', {
            'fields': ('spousename', 'spousepreviousname', 'spouseyear')
        }),
        ('Note', {
            'fields': ('classnote', 'picture', 'cropping', 'caption', 'alumnicomments')
        }),
        ('Publication Information', {
            'fields': ('category','alumnistatus', 'pubstatus', 'pubstatusdate', 'carthaginianstatus')
        }),
    )

    actions = ['set_carthiginian_status']

    def save_model(self, request, obj, form, change):
        obj.save()
        if "alumnistatus" in form.changed_data:
            if obj.alumnistatus:
                if settings.DEBUG:
                    TO_LIST = [settings.SERVER_EMAIL]
                else:
                    TO_LIST = settings.ALUMNI_CLASSNOTES_EMAILS
                email = settings.DEFAULT_FROM_EMAIL
                subject = "[Alumni Class Notes] Alumni Office has approved this note"
                frum = email
                send_mail(
                    request,
                    TO_LIST,
                    subject,
                    frum,
                    "alumni/classnotes/email.html",
                    obj,
                    reply_to=[frum,],
                    bcc=[settings.MANAGERS[0][1]],
                )

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

