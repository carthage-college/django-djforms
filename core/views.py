from django.template import RequestContext
from django.template import loader, Context
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from djforms.core.models import GenericContactForm, GenericChoice
from djforms.core.forms import *

from types import *

def data_entered(request):
    return render_to_response('eduform/data_entered.html')
    
def add_object(request, slug):
    gform = get_object_or_404(GenericContactForm,slug=slug)
    form = None
    if request.method == 'POST':
        form = eval(gform.form_class)(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect ('/eduform/data-entered')
    else:
        form = eval(gform.form_class)()
    return render_to_response("eduform/add_form.html", {'form':form,'gform':gform}, context_instance=RequestContext(request))
