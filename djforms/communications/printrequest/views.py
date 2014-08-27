from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djtools.utils.mail import send_mail, EmailMessage

from djforms.communications.printrequest.forms import PrintRequestForm

def print_request(request):
    if settings.DEBUG:
        TO_LIST = ["zwenta@carthage.edu",]
    else:
        TO_LIST = ["zwenta@carthage.edu",]
        
    if request.method == 'POST':
        form = PrintRequestForm(request.POST)
        if form.is_valid():
            data = form.save()
            
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']
            file3 = request.FILES['file3']
            file4 = request.FILES['file4']
            
            try:
                mail = EmailMessage("test", "testing form submission", TO_LIST, "test@test.com")
                mail.attach(file1.name, attach.read(), file1.content_type)
                mail.attach(file2.name, attach.read(), file2.content_type)
                mail.attach(file3.name, attach.read(), file3.content_type)
                mail.attach(file4.name, attach.read(), file4.content_type)
                mail.send()
                
            except:
                return "Attachment error"
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
