from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy

from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

from djforms.communications.metamorphosis.forms import ParentQuestionnaireForm
from djforms.communications.metamorphosis.forms import StudentQuestionnaireForm
from djforms.communications.metamorphosis.models import Questionnaire
from djforms.core.models import Photo


def questionnaire_form(request, who):
    form = str_to_class(
        "djforms.communications.metamorphosis.forms",
        "{}QuestionnaireForm".format(who.capitalize())
    )
    if not form:
        raise Http404

    if request.method=="POST":
        form = form(request.POST)
        if form.is_valid():
            data = form.save()
            photos = request.FILES.getlist("photos[]")
            captions = request.POST.getlist("captions[]")
            counter=0
            for photo in photos:
                filename = photo.name
                photo.name = photo.name.replace(' ', '')
                p = Photo(title=photo.name, caption=captions[counter])
                p.original.save(photo.name, ContentFile(photo.read()))
                data.photos.add(p)
                counter = counter + 1
            data.save()

            if settings.DEBUG:
                TO_LIST = [settings.SERVER_EMAIL,]
            else:
                TO_LIST = settings.COMMUNICATIONS_METAMORPHOSIS_TO_LIST
            subject = u"[Next Step: The world] {}".format(
                    data.student_name
            ).encode("utf-8")
            send_mail(
                request, TO_LIST, subject, data.email,
                "communications/metamorphosis/email.html",
                data, settings.MANAGERS
            )
            return HttpResponseRedirect(
                reverse_lazy("metamorphosis_questionnaire_success")
            )

    return render_to_response(
        "communications/metamorphosis/form.html",
        {"form":form, "who":who},
        context_instance=RequestContext(request)
    )

def questionnaire_detail(request, quid):
    """
    Simple view to display the questionnaire detail
    """

    mq = get_object_or_404(Questionnaire, id=quid)

    template_name = "communications/metamorphosis/detail.html"
    return render_to_response(
        template_name, {'data':mq,},
        context_instance=RequestContext(request)
    )
