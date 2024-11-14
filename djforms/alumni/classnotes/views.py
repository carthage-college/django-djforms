# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djforms.alumni.classnotes.forms import ContactForm
from djforms.alumni.classnotes.models import Contact
from djtools.utils.mail import send_mail
from PIL import Image


@csrf_exempt
def rotate_photo(request):
    """AJAX Post request for rotating an image 90 degrees clockwise."""
    msg = "Could not find contact with that ID"
    cid = request.POST.get('cid')
    try:
        contact = Contact.objects.get(pk=cid)
    except Exception:
        contact = None
    if contact:
        photo = contact.picture.path
        thumb = contact.thumbnail.path
        # photo
        if photo.lower().split('.')[-1] in {'jpg', 'jpeg', 'png'}:
            try:
                src_im = Image.open(photo)
                im = src_im.rotate(settings.ROTATE_PHOTO, expand=True)
                im.save(photo)
                msg = "Success"
            except Exception:
                msg = "Something is amiss with that graphics file."
        # thumb
        if msg == 'Success' and thumb.lower().split('.')[-1] in {'jpg', 'jpeg', 'png'}:
            try:
                src_im = Image.open(thumb)
                im = src_im.rotate(settings.ROTATE_PHOTO, expand=True)
                im.save(thumb)
                msg = "Success"
            except Exception:
                msg = "Something is a miss with that file."
        else:
            msg = "Something is amiss with the thumbnail file."

    return HttpResponse(
        msg, content_type='text/plain; charset=utf-8',
    )


def contact(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = settings.ALUMNI_CLASSNOTES_EMAILS

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, use_required_attribute=False)
        if form.is_valid():
            contact = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if contact.email:
                email = contact.email
            subject = "[Alumni Class Notes] {0} {1}".format(
                contact.first_name, contact.last_name,
            )
            frum = email
            send_mail(
                request,
                TO_LIST,
                subject,
                frum,
                'alumni/classnotes/email.html',
                contact,
                reply_to=[frum,],
                bcc=[settings.MANAGERS[0][1],],
            )
            return HttpResponseRedirect(reverse_lazy('classnotes_success'))
    else:
        form = ContactForm(use_required_attribute=False)
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/form.html',
        {'form': form, 'manager': manager},
    )


def archives(request, year=None):
    """Decade based archives."""
    if year:
        year = int(year)
    else:
        year = 2020

    ns = Contact.objects.exclude(pubstatus=False).exclude(
        category='Death Announcement',
    ).exclude(classnote__exact='None')
    notes = ns.filter(classyear__range=[year, year + 9]).order_by(
        '-classyear', '-created_at',
    )
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'year': year, 'manager': manager},
    )


def screenscrape(request):
    ns = Contact.objects.exclude(carthaginianstatus=True)
    notes = ns.order_by('classyear', 'last_name')
    manager = request.user.has_perm('classnotes.change_contact')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'title': 'Carthaginian', 'manager': manager},
    )


def obits(request):
    obs = Contact.objects.filter(category='Death Announcement')
    notes = obs.order_by('-classyear', 'last_name')

    return render(
        request,
        'alumni/classnotes/archives.html',
        {'notes': notes, 'title': 'In Memoriam'},
    )
