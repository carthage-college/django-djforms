# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from djauth.managers import LDAPManager
from djforms.music.ensembles.choral.models import Candidate
from djforms.music.ensembles.choral.models import TimeSlot


TIME_SLOTS = TimeSlot.objects.filter(active=True).order_by('id')


class CandidateForm(forms.ModelForm):
    """Form class for the choral tryout form."""

    time_slot = forms.ModelChoiceField(queryset=TIME_SLOTS)

    class Meta:
        model = Candidate
        exclude = ('user', 'created_on', 'updated_on')


class ManagerForm(CandidateForm):
    """Form class to allow managers to submit the form."""

    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField()

    class Meta:
        model = Candidate
        exclude = ('user', 'created_on', 'updated_on')
        fields = (
            'first_name',
            'last_name',
            'email',
            'time_slot',
            'majors',
            'grad_year',
            'experience',
        )

    def clean(self):
        """Check for a valid user or try to create one."""
        cd = self.cleaned_data
        error = None
        if cd.get('email'):
            # search for a valid user
            eldap = LDAPManager()
            username = cd['email'].split('@')[0]
            user = User.objects.filter(username=username).first()
            if not user:
                result_data = eldap.search(username, field='cn')
                if result_data:
                    # deal with groups
                    groups = eldap.get_groups(result_data)
                    # Create a User object.
                    user = eldap.dj_create(
                        result_data,
                        auth_user_pk=settings.LDAP_AUTH_USER_PK,
                        groups=groups,
                    )
                else:
                    error = "Please confirm that the email address is correct"
            if user:
                # check for username change:
                if user.username != username:
                    user.username = username
                    user.save()
        else:
            error = "Please provide a valid email address",
        if error:
            self.add_error('email', error)
