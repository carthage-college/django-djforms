from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djtools.utils.mail import send_mail

from djforms.communications.printrequest.forms import PrintRequestForm

def print_request(request):
    if request.method == 'POST':
        form = PrintRequestForm(request.POST)
        if form.is_valid():
            data = form.save()
            return HttpResponseRedirect(reverse('success'))
    else:
        form = PrintRequestForm()
    return render_to_response(
        'communications/printrequest/form.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
