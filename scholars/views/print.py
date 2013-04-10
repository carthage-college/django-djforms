from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from djforms.scholars.models import Presentation


def alpha(request, template=None):
    presentations = Presentation.objects.all().order_by('leader__last_name')

    if not template:
        template = "scholars/print/pdf.html"
    return render_to_response (
        template, {"presentations": presentations,},
        context_instance=RequestContext(request)
    )

def presenters(request):
    students = Student.objects.all().order_by('shirt')
    faculty = Faculty.objects.all().order_by('shirt')

    return render_to_response("manager/presenters.html", {"students": students, "faculty":faculty, }, context_instance=RequestContext(request))