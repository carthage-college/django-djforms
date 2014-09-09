from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.polisci.wipcs.proposal.forms import ProposalContactForm
from djforms.polisci.wipcs import TO_LIST, BCC
from djtools.utils.mail import send_mail

def form(request):
    """
    Proposal form
    """
    if request.POST:
        form = ProposalContactForm(request.POST,request.FILES)
        if form.is_valid():
            contact = form.save()
            send_mail(
                request, TO_LIST,
                "[WIPCS] Conference Proposal", contact.email,
                "polisci/wipcs/proposal/email.html", contact, BCC
            )
            return HttpResponseRedirect(
                reverse('wipcs_proposal_success')
            )
    else:
        form = ProposalContactForm()
    return render_to_response(
        'polisci/wipcs/proposal/form.html', {
            'form': form,
        }, context_instance=RequestContext(request))

