from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.polisci.iea.proposal.forms import ProposalContactForm
from djforms.polisci.iea import TO_LIST, BCC
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
                "[IEA] Conference Proposal", contact.email,
                'polisci/iea/proposal/email.html', contact, BCC
            )
            return HttpResponseRedirect(
                reverse('iea_proposal_success')
            )
    else:
        form = ProposalContactForm()

    return render(
        request, 'polisci/iea/proposal/form.html', {
            'form': form,
        }
    )

