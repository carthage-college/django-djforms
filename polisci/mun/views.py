from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

def registration_form(request):
    form=''
    return render_to_response("polisci/mun/registration_form.html", {"form": form,}, context_instance=RequestContext(request))
