from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djforms.polisci.iea.proposal.forms import ProposalContactForm
from djforms.polisci.iea.proposal.forms import ProposalOrderForm
from djforms.processors.forms import TrustCommerceForm

from djforms.polisci.iea import TO_LIST, BCC
from djtools.utils.mail import send_mail


def form(request):
    """
    Abstract Proposal form
    """
    if request.POST:
        form_con =ProposalContactForm(request.POST)
        form_ord = ProposalOrderForm(request.POST)
        if form_con.is_valid() and form_ord.is_valid():
            contact = form_con.save()
            order = form_ord.save()
            order.operator = settings.POLITICAL_SCIENCE_IEA_OPERATOR
            if contact.payment_method == 'Credit Card':

                form_proc = TrustCommerceForm(
                    order, contact, request.POST, use_required_attribute=False
                )

                if form_proc.is_valid():
                    r = form_proc.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.cc_name = form_proc.name
                    order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
                    order.reg = contact
                    order.contact = contact
                    reg = order.contact.registration_fee.split('|')
                    order.contact.registration_fee = '{} (${})'.format(
                        reg[0],reg[1]
                    )
                    sent = send_mail(
                        request, TO_LIST,
                        "[IEA] Conference Registration", contact.email,
                        'polisci/iea/registration/email.html', order, BCC
                    )
                    order.send_mail = sent
                    order.save()

                    return HttpResponseRedirect(
                        reverse('iea_registration_success')
                    )

                else:
                    r = form_proc.processor_response
                    if r:
                        order.status = r.status
                    else:
                        order.status = 'Form Invalid'
                    order.cc_name = form_proc.name
                    if form_proc.card:
                        order.cc_4_digits = form_proc.card[-4:]
                    order.save()
                    contact.order.add(order)
            else:
                order.auth='COD'
                order.status='Pay later'
                order.save()
                contact.order.add(order)
                order.reg = contact
                order.contact = contact

                send_mail(
                    request, TO_LIST,
                    "[IEA] Conference Abstract Proposal", contact.email,
                    'polisci/iea/proposal/email.html', order, BCC
                )

                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(
                    reverse('iea_proposal_success')
                )
        else:
            if request.POST.get('payment_method') == 'Credit Card':
                form_proc = TrustCommerceForm(
                    None, request.POST, use_required_attribute=False
                )
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm(use_required_attribute=False)
    else:
        form_con = ProposalContactForm()
        form_ord = ProposalOrderForm(
            initial={'total':50, 'avs':False,'auth':'sale'}
        )
        form_proc = TrustCommerceForm(use_required_attribute=False)

    return render(
        request, 'polisci/iea/proposal/form.html', {
            'form_con': form_con, 'form_ord':form_ord,
            'form_proc':form_proc
        }
    )
