# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from djforms.contact.models import Message


class ContactForm(forms.Form):
    name = forms.CharField(label=_('name'), max_length=60)
    mail = forms.EmailField(label=_('email'))
    subject = forms.CharField(label=_('subject'),
                              max_length=100,
                              required=False)
    message = forms.CharField(label=_('message'), widget=forms.Textarea)

    class Media:
        js = ('js/contact.js',)

    def get_context(self):
        pass

    def send(self, slug, fail_silently=False):
        if self.is_valid():
            cm = Message(name=self.cleaned_data['name'],
			 mail=self.cleaned_data['mail'],
			 subject=self.cleaned_data['subject'],
			 message=self.cleaned_data['message'])
            cm.send(slug, fail_silently=fail_silently)
        else:
            raise ValueError(_('can\'t send a message if form isn\'t valid'))
