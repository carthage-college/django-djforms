from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy

from djtools.utils.mail import send_mail
from djforms.alumni.memory.forms import *
from djforms.alumni.memory.models import Questionnaire
from djforms.core.models import Photo, Promotion

import datetime

def questionnaire_form(request, campaign=None):
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
        slug_list = campaign.slug.split("-")
        form_name = slug_list.pop(0).capitalize()
        for n in slug_list:
            form_name += "{}".format( n.capitalize() )
    else:
        campaign = ""
        form_name = "QuestionnaireForm"

    try:
        form = eval(form_name)()
    except:
        raise Http404

    if request.method=="POST":

        try:
            form = eval(form_name)(
                data=request.POST, files=request.FILES
            )
        except:
            # form_name does not match an existing form
            raise Http404

        if form.is_valid():
            memory = form.save()
            category = "Alumni Questionnaire Detail"
            if campaign:
                memory.promotion = campaign
                category = campaign.title
            photos = request.FILES.getlist("photos[]")
            captions = request.POST.getlist("captions[]")
            counter=0
            for photo in photos:
                filename = photo.name
                photo.name = photo.name.replace(' ', '')
                p = Photo(title=photo.name, caption=captions[counter])
                p.original.save(photo.name, ContentFile(photo.read()))
                memory.photos.add(p)
                counter = counter + 1
            memory.save()

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL,]
            else:
                TO_LIST = ["lhansen@carthage.edu",]
            send_mail(
                request, TO_LIST,
                "[{}] {} {}".format(
                    category, memory.first_name, memory.last_name
                ), memory.email,
                "alumni/memory/email.html",
                memory, settings.MANAGERS
            )
            return HttpResponseRedirect(
                reverse_lazy("memory_questionnaire_success")
            )

    return render_to_response(
        "alumni/memory/form.html",
        {"form": form,"campaign":campaign},
        context_instance=RequestContext(request)
    )

def questionnaire_detail(request, quid):
    """
    Simple view to display the questionnaire detail
    """

    mq = get_object_or_404(Questionnaire, id=quid)

    template_name = "alumni/memory/detail.html"
    return render_to_response(
        template_name, {'data': mq,},
        context_instance=RequestContext(request)
    )
