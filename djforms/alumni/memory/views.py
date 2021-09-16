# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from djforms.alumni.memory.forms import *
from djforms.alumni.memory.models import Questionnaire
from djforms.core.models import Photo
from djforms.core.models import Promotion
from djtools.utils.convert import str_to_class
from djtools.utils.mail import send_mail


def questionnaire_form(request, campaign=None):
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
        slug_list = campaign.slug.split('-')
        form_name = slug_list.pop(0).capitalize()
        for n in slug_list:
            form_name += '{0}'.format( n.capitalize() )
    else:
        campaign = ''
        form_name = 'QuestionnaireForm'

    form = str_to_class('djforms.alumni.memory.forms', form_name)()
    if not form:
        raise Http404

    if request.method=='POST':

        form = str_to_class(
            'djforms.alumni.memory.forms', form_name,
        )(data=request.POST, files=request.FILES)

        if not form:
            # form_name does not match an existing form
            raise Http404

        if form.is_valid():
            memory = form.save()
            category = 'Alumni Questionnaire Detail'
            if campaign:
                memory.promotion = campaign
                category = campaign.title
            photos = request.FILES.getlist('photos[]')
            captions = request.POST.getlist('captions[]')
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
                TO_LIST = settings.ALUMNI_MEMORY_EMAIL
            send_mail(
                request, TO_LIST,
                '[{0}] {1} {2}'.format(
                    category, memory.first_name, memory.last_name,
                ), memory.email,
                'alumni/memory/email.html',
                memory,
                settings.MANAGERS,
            )
            return HttpResponseRedirect(
                reverse_lazy('memory_questionnaire_success'),
            )

    return render(
        request,
        'alumni/memory/form.html',
        {'form': form,'campaign':campaign},
    )


def questionnaire_detail(request, quid):
    """Simple view to display the questionnaire detail."""
    mq = get_object_or_404(Questionnaire, id=quid)

    template_name = 'alumni/memory/detail.html'

    return render(request, template_name, {'data': mq})


def questionnaire_archives(request):
    """Simple view to display all of the questionnaires."""
    objects = Questionnaire.objects.all().order_by('promotion', '-created_at')
    template_name = 'alumni/memory/archives.html'
    return render(request, template_name, {'objects': objects})
