from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.core.files.base import ContentFile

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

            recipient_list = ["skirk@carthage.edu", "mfisher@carthage.edu"]
            """
            managers = User.objects.filter(groups__id__in=[2,3])
            for m in managers:
                perms = m.get_profile().permission.filter(name=maintenance_request.type_of_request.name)
                if perms:
                    recipient_list.append(m.email)
            """
            t = loader.get_template('alumni/memory/questionnaire_email.txt')
            c = RequestContext(request, {'data':memory,})
            send_mail(("Alumni Memory Questionnaire Detail: %s, %s" % (memory.last_name, memory.first_name)), t.render(c), memory.email, recipient_list, fail_silently=False)

            return HttpResponseRedirect('/forms/alumni/data-entered')
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
