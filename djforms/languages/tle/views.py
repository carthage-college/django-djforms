# -*- coding: utf-8 -*-
from django.http import Http404
from django.conf import settings
from django.utils.dates import MONTHS
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from djforms.languages.tle.forms import *

from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

import datetime


def application_form(request, stype):
    form_name = '{0}Form'.format(stype.capitalize())
    form = str_to_class('djforms.languages.tle.forms', form_name)()
    if not form:
        raise Http404

    education = ''
    ulength = 1
    if request.method == 'POST':
        form = str_to_class('djforms.languages.tle.forms', form_name)(request.POST)
        # check if someone is attempting something nefarious
        if not form:
            raise Http404
        data = request.POST.copy()
        if form.is_valid():
            cd = form.cleaned_data
            if stype == 'masters':
                education = ''
                # collect our university fields
                university = data.getlist('university[]')
                country = data.getlist('country[]')
                from_month = data.getlist('from_month[]')
                to_month = data.getlist('to_month[]')
                from_year = data.getlist('from_year[]')
                to_year = data.getlist('to_year[]')
                degree = data.getlist('degree[]')
                # establish the number of universities submitted
                # and iterate over them to build education
                for index in range(len(university)):
                    education += '<dl>'
                    education += '''
                        <dt>University</dt><dd>{0}</dd>
                    '''.format(university[index])
                    education += '<dt>Country</dt><dd>{0}</dd>'.format(
                        country[index],
                    )
                    education += '''
                        <dt>From</dt><dd>{0} {1}</dd>
                    '''.format(from_month[index], from_year[index])
                    education += '''
                        <dt>To</dt><dd>{0} {1}</dd>
                    '''.format(to_month[index], to_year[index])
                    education += '<dt>Degree</dt><dd>{0}</dd>'.format(
                        degree[index]
                    )
                    education += '</dl>'
                cd['education'] = education
            cd['type'] = stype

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL]
            else:
                TO_LIST = settings.MODERN_LANGUAGES_TLE_APPLICATIONS
                TO_LIST.append(cd['email'])

            subject = '[Modern Languages] TLE {0}: {1} {2}'.format(
                stype.capitalize(), cd['first_name'], cd['last_name'],
            )

            send_mail(
                request,
                TO_LIST,
                subject,
                cd['email'],
                'languages/tle/email.html',
                cd,
                settings.MANAGERS,
            )
            return HttpResponseRedirect(reverse_lazy('tle_success'))
        elif stype == 'masters':
            # collect our fields
            university = data.getlist('university[]')
            country = data.getlist('country[]')
            from_month = data.getlist('from_month[]')
            to_month = data.getlist('to_month[]')
            from_year = data.getlist('from_year[]')
            to_year = data.getlist('to_year[]')
            degree = data.getlist('degree[]')
            # establish the number of universities submitted
            # and iterate over them to build our form parts
            ulength = len(university)
            for index in range(ulength):
                if len(university) == 1 or index == 0:
                    education += '<ol id="universities">'
                elif index > 0:
                    num = int(index) - 1
                    education += '<ol id="universities{}">'.format(str(num))
                education += '<li class="ctrlHolder"><h3>University Name</h3><input type="text" name="university[]" value="{0}" />'.format(university[index])
                education += '<li class="ctrlHolder"><h3>Country</h3><input type="text" name="country[]" value="{0}" />'.format(country[index])
                education += '<li class="ctrlHolder"><h3>From</h3>'
                education += '<select name="from_month[]" class="small">'
                options_month = ''
                for month in range(len(MONTHS)):
                    selected = ''
                    if MONTHS[month+1] == from_month[index]:
                        selected = ' selected="selected"'
                    options_month += '<option value="{0}"{1}>{2}</option>'.format(MONTHS[month+1], selected, MONTHS[month+1])
                education += options_month
                education += '</select>'
                education += 'Year <input type="text" class="small" name="from_year[]" value="{0}" />'.format(from_year[index])
                education += '</li>'
                education += '<li class="ctrlHolder"><h3>To</h3>'
                education += '<select name="to_month[]" class="small">'
                options_month = ''
                for month in range(len(MONTHS)):
                    selected = ''
                    if MONTHS[month+1] == to_month[index]:
                        selected = ' selected="selected"'
                    options_month += '<option value="{0}"{1}>{2}</option>'.format(
                        MONTHS[month+1], selected, MONTHS[month+1],
                    )
                education += options_month
                education += '</select>'
                education += 'Year <input type="text" class="small" name="to_year[]" value="{0}" />'.format(to_year[index])
                education += '</li>'
                education += '<li class="ctrlHolder"><h3>Diploma/Degree</h3><input type="text" name="degree[]" value="{0}" /></li>'.format(degree[index])
                education += '<li class="ctrlHolder"><hr /></li>'
                education += '</ol>'
    return render(
        request,
        'languages/tle/form.html',
        {
            'form': form,
            'type': stype,
            'months': MONTHS,
            'education': education,
            'length': ulength,
        }
    )
