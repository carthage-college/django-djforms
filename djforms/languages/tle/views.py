from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import Http404
from django.utils.dates import MONTHS
from django.core.urlresolvers import reverse_lazy

from djforms.languages.tle.forms import *

import datetime

def application_form(request, stype):
    form_name = stype.capitalize() + "Form"
    try:
        #form = form = eval(form_name)()
        form = eval(form_name)()
    except:
        raise Http404

    education = ''
    ulength = 1
    if request.method=='POST':
        form = eval(form_name)(request.POST)
        cd = request.POST.copy()
        if form.is_valid():
            education=''
            if stype=="masters":
                # collect our university fields
                university = cd.getlist('university[]')
                country = cd.getlist('country[]')
                from_month = cd.getlist('from_month[]')
                to_month = cd.getlist('to_month[]')
                from_year = cd.getlist('from_year[]')
                to_year = cd.getlist('to_year[]')
                degree = cd.getlist('degree[]')
                # establish the number of universities submitted
                # and iterate over them to build education
                for index in range(len(university)):
                    education += '<dl>'
                    education += '''
                        <dt>University</dt><dd>%s</dd>
                    ''' % university[index]
                    education += '<dt>Country</dt><dd>%s</dd>' % country[index]
                    education += '''
                        <dt>From</dt><dd>%s %s</dd>
                    ''' % (from_month[index],from_year[index])
                    education += '''
                        <dt>To</dt><dd>%s %s</dd>
                    ''' % (to_month[index],to_year[index])
                    education += '<dt>Degree</dt><dd>%s</dd>' % degree[index]
                    education += '</dl>'
            cd = form.cleaned_data
            bcc = settings.MANAGERS
            to = ["sgrover@carthage.edu","emontanaro@carthage.edu",cd['email']]
            t = loader.get_template('languages/tle/email.txt')
            c = RequestContext(
                request, {'data':cd,'education':education,'type':stype}
            )
            email = EmailMessage(
                ("[Modern Languages] %s Application: %s %s" % (stype.capitalize(),cd['first_name'],cd['last_name'])),
                t.render(c), cd['email'], to, bcc,
                headers = {'Reply-To': cd['email'],'From': cd['email']}
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect(
                reverse_lazy("tle_success")
            )
        elif stype=="masters":
            # collect our fields
            university = cd.getlist('university[]')
            country = cd.getlist('country[]')
            from_month = cd.getlist('from_month[]')
            to_month = cd.getlist('to_month[]')
            from_year = cd.getlist('from_year[]')
            to_year = cd.getlist('to_year[]')
            degree = cd.getlist('degree[]')
            # establish the number of universities submitted
            # and iterate over them to build our form parts
            ulength = len(university)
            for index in range(ulength):
                if len(university) == 1 or index == 0:
                    education += '<ol id="universities">'
                elif index > 0:
                    num = int(index)-1
                    education += '<ol id="universities%s">' % str(num)
                education += '<li class="ctrlHolder"><h3>University Name</h3><input type="text" name="university[]" value="%s" />' % university[index]
                education += '<li class="ctrlHolder"><h3>Country</h3><input type="text" name="country[]" value="%s" />' % country[index]
                education += '<li class="ctrlHolder"><h3>From</h3>'
                education += '<select name="from_month[]">'
                options_month = ''
                for month in range(len(MONTHS)):
                    selected=''
                    if unicode(MONTHS[month+1])==from_month[index]:
                        selected=' selected="selected"'
                    options_month += '<option value="%s"%s>%s</option>' % (unicode(MONTHS[month+1]),selected,unicode(MONTHS[month+1]))
                education += options_month
                education += '</select>'
                education += 'Year <input type="text" name="from_year[]" value="%s" />' % from_year[index]
                education += '</li>'
                education += '<li class="ctrlHolder"><h3>To</h3>'
                education += '<select name="to_month[]">'
                options_month = ''
                for month in range(len(MONTHS)):
                    selected=''
                    if unicode(MONTHS[month+1])==to_month[index]:
                        selected=' selected="selected"'
                    options_month += '<option value="%s"%s>%s</option>' % (unicode(MONTHS[month+1]),selected,unicode(MONTHS[month+1]))
                education += options_month
                education += '</select>'
                education += 'Year <input type="text" name="to_year[]" value="%s" />' % to_year[index]
                education += '</li>'
                education += '<li class="ctrlHolder"><h3>Diploma/Degree</h3><input type="text" name="degree[]" value="%s" /></li>' % degree[index]
                education += '<li class="ctrlHolder"><hr /></li>'
                education += '</ol>'

    return render_to_response(
        "languages/tle/form.html", {
            "form": form,'type':stype,'months':MONTHS,
            'education':education,'length':ulength
        },
        context_instance=RequestContext(request)
    )
