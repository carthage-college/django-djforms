from django.conf import settings
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djforms.communications.printrequest.forms import PrintRequestForm
from djtools.utils.mail import send_mail

@login_required
def print_request(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = ["communications@carthage.edu",]

    if request.method == 'POST':
        form = PrintRequestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.updated_by = request.user
            data.save()
            if not settings.DEBUG:
                TO_LIST.append(data.user.email)
                subject = u"[Print request] {}: {}".format(
                    data.project_name, data.date_created
                ).encode('utf-8').strip()
                send_mail(
                    request, TO_LIST,
                    subject, data.user.email,
                    "communications/printrequest/email.html", data,
                    settings.MANAGERS
                )
                return HttpResponseRedirect(reverse('print_request_success'))
            else:
                return render_to_response(
                    'communications/printrequest/email.html',
                    {
                        'data': data,
                    },
                    context_instance=RequestContext(request)
                )
    else:
        form = PrintRequestForm()
    return render_to_response(
        'communications/printrequest/form.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
