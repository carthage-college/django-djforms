from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from djforms.maintenance.forms import EVSForm, EVSFormUpdate
from djforms.maintenance.models import MaintenanceRequest
from djforms.core.forms import UserProfileForm
from djforms.core.models import GenericChoice

from operator import attrgetter
from itertools import chain
from tagging.models import Tag, TaggedItem

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO,)

@login_required
def maintenance_request_form(request):
    if request.method=='POST':
        try:
            profile = request.user.get_profile()
        except:
            logging.debug("username = %s" % request.user.username)
            profile = ''
        #   p = UserProfile(user=request.user)
        #   p.save()
        #   profile = request.user.get_profile()
        form = EVSForm(request.POST, prefix="evs")
        profile_form = UserProfileForm(request.POST, prefix="profile", instance=profile)
        if form.is_valid() and profile_form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.user = request.user

            maintenance_request.status = 'New'
            maintenance_request.save()
            form.save_m2m()
            profile_form.save()
            bcc = settings.MANAGERS
            recipient_list = ["jramirez@carthage.edu"]

            managers = User.objects.filter(groups__id__in=[2,3])
            for m in managers:
                perms = m.get_profile().permission.filter(name=maintenance_request.type_of_request.name)
                if perms:
                    recipient_list.append(m.email)

            reviewers = User.objects.filter(groups__id=4)
            for r in reviewers:
                perms = r.get_profile().permission.filter(name=maintenance_request.building.name)
                if perms:
                    recipient_list.append(r.email)

            t = loader.get_template('maintenance/email.txt')
            c = Context({'data':maintenance_request,})
            email = EmailMessage(("[Maintenance ID: %s] %s Floor %s Room %s: %s" % (str(maintenance_request.id), maintenance_request.building.name, maintenance_request.floor, maintenance_request.room_number, maintenance_request.type_of_request.name)), t.render(c), request.user.email, recipient_list, bcc, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.send(fail_silently=True)

            return HttpResponseRedirect('/forms/maintenance/success')
    else:
        form = EVSForm(prefix="evs")
        profile_form = UserProfileForm(prefix="profile")
    return render_to_response("maintenance/maintenance_form.html", {"form": form,"profile_form": profile_form}, context_instance=RequestContext(request))

@login_required
def maintenance_requests(request):
    """
    Simple view to display all requests from the current user
    """

    # set up our permissions base via tags
    # building name tag
    building_name_tag = Tag.objects.get(name__iexact='Building Name')
    #building_perms = TaggedItem.objects.get_by_model(request.user.get_profile().permission.all(), building_name_tag).filter(active=True)
    building_perms = TaggedItem.objects.get_by_model(request.user.get_profile().permission.all(), building_name_tag)
    bpids = []
    for p in building_perms:
        bpids.append(p.id)
    # type of request tag
    type_of_request_tag = Tag.objects.get(name__iexact='Maintenance Request Type')
    #type_perms = TaggedItem.objects.get_by_model(request.user.get_profile().permission.all(), type_of_request_tag).filter(active=True)
    type_perms = TaggedItem.objects.get_by_model(request.user.get_profile().permission.all(), type_of_request_tag)
    tpids = []
    for p in type_perms:
        tpids.append(p.id)

    # superuser or manager
    if request.user.is_superuser or request.user.groups.filter(id=2):
        my_reqs = MaintenanceRequest.objects.all().order_by("-date_created")
    # editors
    elif request.user.groups.filter(id=3):
        type_reqs = MaintenanceRequest.objects.filter(type_of_request__in=tpids)
        # check to see if our editor is also a reviewer, and if so, add reqs
        if request.user.groups.filter(id=4):
            building_reqs = MaintenanceRequest.objects.filter(building__in=bpids).exclude(type_of_request__in=tpids)
        else:
            building_reqs = MaintenanceRequest.objects.none()
        my_reqs = sorted(
            chain(type_reqs, building_reqs),
            key=attrgetter('date_created'), reverse=True)
    # reviewers
    elif request.user.groups.filter(id=4):
        my_reqs = MaintenanceRequest.objects.filter(type_of_request__in=bpids)
    # student
    else:
        my_reqs = MaintenanceRequest.objects.filter(user__username=request.user.username).order_by("-date_created")
    return render_to_response("maintenance/maintenance_requests.html", {"my_reqs": my_reqs,}, context_instance=RequestContext(request))

@login_required
def maintenance_request_detail(request, req_id):
    """
    Simple view to display the  request detail
    """

    mr = get_object_or_404(MaintenanceRequest, id=req_id)

    auth = False
    # superuser, manager, editor
    if request.user.is_superuser or request.user.groups.filter(id__in=[1,2,3]):
        auth = True
    else:
        if mr.user.id == request.user.id:
            auth = True

    template_name = "maintenance/maintenance_detail.html"
    return render_to_response(template_name, {
        'mr': mr,
        'auth': auth,
    }, context_instance=RequestContext(request))

@staff_member_required
def maintenance_request_update(request, req_id):
    """
    Simple view to update the request detail
    """

    mr = get_object_or_404(MaintenanceRequest, id=req_id)

    if request.method == 'POST':
        form = EVSFormUpdate(request.POST, instance=mr)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.updated_by = request.user
            maintenance_request.save()
            form.save_m2m()
            return HttpResponseRedirect('/forms/maintenance/success')
    else:
        form = EVSFormUpdate(instance=mr)

    return render_to_response("maintenance/maintenance_update_form.html", {"form": form,'mr': mr,}, context_instance=RequestContext(request))
