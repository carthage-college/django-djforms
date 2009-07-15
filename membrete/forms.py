# -*- coding: utf-8 -*-

# Copyright © 2009 Gonzalo
#
# This file is part of membrete.
#
# membrete is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# membrete is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with membrete. If not, see
# <http://www.gnu.org/licenses/>.

from django import forms
from django.utils.translation import ugettext_lazy as _
from djforms.membrete.models import Message


class ContactForm(forms.Form):
    name = forms.CharField(label=_('name'), max_length=60)
    mail = forms.EmailField(label=_('email'))
    subject = forms.CharField(label=_('subject'),
                              max_length=100,
                              required=False)
    message = forms.CharField(label=_('message'), widget=forms.Textarea)

    class Media:
        js = ('js/membrete.js',)

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
