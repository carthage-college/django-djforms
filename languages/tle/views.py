from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import Http404
from django.utils.dates import MONTHS

from djforms.languages.tle.forms import *

import datetime

def application_form(request, type):
    form_name = type.capitalize() + "Form"
    try:
        form = form = eval(form_name)()
    except:
        raise Http404

    if request.method=='POST':
        form = eval(form_name)(request.POST)
        cd = request.POST.copy()
        if form.is_valid():
            cd = form.cleaned_data
            bcc = settings.MANAGERS
            #to = ["mrothstein@carthage.edu",request.user.email]
            to = ["skirk@carthage.edu"]
            t = loader.get_template('languages/tle/application_email.txt')
            c = RequestContext(request, {'data':cd,'user':request.user,'date':datetime.date.today(),'type':type})
            email = EmailMessage(("[Modern Languages] %s Application: %s %s" % (type.capitalize(),cd['first_name'],cd['last_name'])), t.render(c), request.user.email, to, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/languages/success')
        else:
            university = cd.getlist('university[]')
            length_uni = len(universities)
            for index in range(len(length_uni)):
                if length_uni == 1 or index == 1:
                    education = '<ol id="universities">'
                elif index > 1:
                    education = '<ol id="universities%s">' % str(index)-2
                education += '<li class="ctrlHolder"><h3>University Name</h3><input type="text" name="university[]" value="%s" />' % university[index]
                education += '<li class="ctrlHolder"><h3>Country</h3><input type="text" name="country[]" value="%s" />' % country[index]
                education += '<li class="ctrlHolder"><h3>From</h3>'
                # need to build a select statement here
                for index in range(len(MONTHS)):
                    print unicode(MONTHS)
                education += 'Year <input type="text" name="from_year[]" value="%s" />' % from_year[index]
                education += '</ol>'
            return render_to_response("languages/tle/application_email.txt", {"data": cd,'user':request.user,'date':datetime.date.today(),'type':type,'education':education}, context_instance=RequestContext(request))

    return render_to_response("languages/tle/application_form.html", {"form": form,'type':type,'months':MONTHS}, context_instance=RequestContext(request))
