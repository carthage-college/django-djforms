from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.core.files.base import ContentFile

from djtools.utils.mail import send_mail
from djforms.alumni.memory.forms import QuestionnaireForm
from djforms.alumni.memory.models import Questionnaire
from djforms.core.models import Photo

import datetime

def questionnaire_form(request):
    if request.method=='POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            memory = form.save()
            photos = request.FILES.getlist('photos[]')
            captions = request.POST.getlist('captions[]')
            counter=0
            for photo in photos:
                filename = photo.name
                photo.name = photo.name.replace(' ', '')
                p = Photo(title=photo.name, caption=captions[counter])
                p.original_image.save(photo.name, ContentFile(photo.read()))
                memory.photos.add(p)
                counter = counter + 1
            memory.save()

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL,]
            else:
                TO_LIST = ["lhansen@carthage.edu",]
            send_mail(
                request, TO_LIST,
                "[Alumni Questionnaire Detail] %s %s" %
                (memory.first_name,memory.last_name),
                memory.email,
                "alumni/memory/questionnaire_email.html",
                memory, settings.MANAGERS
            )

            return HttpResponseRedirect('/forms/alumni/success/')
    else:
        form = QuestionnaireForm()

    return render_to_response("alumni/memory/questionnaire_form.html", {"form": form,}, context_instance=RequestContext(request))

def questionnaire_detail(request, quid):
    """
    Simple view to display the questionnaire detail
    """

    mq = get_object_or_404(Questionnaire, id=quid)

    template_name = "alumni/memory/questionnaire_detail.html"
    return render_to_response(template_name, {'mq': mq,}, context_instance=RequestContext(request))
