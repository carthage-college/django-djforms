from django.conf import settings
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djforms.lis.ito.forms import ProfileForm
from djforms.lis.ito.models import Profile

@login_required
def profile_form(request, id=None):
    profile = None
    if id:
        profile = get_object_or_404(Profile, id=id)
        if (profile.user.id != request.user.id) and not request.user.has_perm('ito.ito_can_manage_profile'):
            raise Http404
    if request.method=='POST':
        if profile:
            form = ProfileForm(request.POST, instance=profile)
        else:
            form = ProfileForm(request.POST)
        if form.is_valid():

            data = form.save(commit=False)
            if not profile:
                data.user = request.user
            data.updated_by = request.user
            data.save()
            # we don't want to send an email if you are a manager
            if not request.user.has_perm('ito.ito_can_manage_profile'):
                users = User.objects.filter(groups__permissions = Permission.objects.get(codename='ito_can_manage_profile')).order_by('-id')
                bcc = []
                for u in users:
                    bcc.append(u.email)
                # TODO: we can make 'from' email more specific if they need it in the future
                frm = bcc[0]
                t = loader.get_template('lis/ito/profile_email.html')
                c = RequestContext(request, {'profile':data,})
                email = EmailMessage(("[Individual Technology Objective] %s %s" % (data.user.first_name,data.user.last_name)), t.render(c), frm, [data.user.email,], bcc, headers = {'Reply-To': frm,'From': frm})
                email.content_subtype = "html"
                email.send()
            ret = '/forms/lis/ito/profile/success/'
            if profile:
                ret = reverse("profile_detail", args=[profile.id])
            return HttpResponseRedirect(ret)
    else:
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()
    return render_to_response("lis/ito/profile_form.html", {"form": form,"id":id,}, context_instance=RequestContext(request))

@staff_member_required
def profile_detail(request, id):
    profile = get_object_or_404(Profile, id=id)
    if (profile.user.id != request.user.id) and not request.user.has_perm('ito.ito_can_manage_profile'):
        raise Http404
    return render_to_response("lis/ito/profile_detail.html", {"profile": profile,}, context_instance=RequestContext(request))

@staff_member_required
@permission_required('ito.ito_can_manage_profile', login_url= '/forms/accounts/login')
def profile_archives(request):
    profiles = Profile.objects.all().order_by("-created_on")
    return render_to_response("lis/ito/profile_archives.html", {"profiles": profiles,}, context_instance=RequestContext(request))
