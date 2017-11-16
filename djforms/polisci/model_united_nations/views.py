from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from djforms.polisci.model_united_nations.forms import AttenderForm
from djforms.polisci.model_united_nations.forms import CountryForm

from djtools.utils.mail import send_mail


def registration(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = settings.POLISCI_MUN_EMAIL_LIST
    BCC = settings.MANAGERS
    if request.method=='POST':
        form_cont = AttenderForm(request.POST, prefix='cont')
        form_pais = CountryForm(request.POST, prefix='pais')
        if form_cont.is_valid() and form_pais.is_valid():
            contact = form_cont.save()
            paises = form_pais.cleaned_data
            contact.delegation_1 = paises['delegation_1']
            contact.delegation_2 = paises['delegation_2']
            contact.delegation_3 = paises['delegation_3']
            contact.delegation_4 = paises['delegation_4']
            contact.delegation_5 = paises['delegation_5']
            contact.save()
            data = {'object':contact}
            subject = "[Model United Nations Registration] {} {} of {}".format(
                contact.first_name, contact.last_name, contact.school_name
            )
            send_mail(
                request, TO_LIST, subject, contact.email,
                'polisci/model_united_nations/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('model_united_nations_success')
            )
    else:
        form_cont = AttenderForm(prefix='cont')
        form_pais = CountryForm(prefix='pais')

    return render(
        request,
        'polisci/model_united_nations/form.html', {
            'form_cont':form_cont,'form_pais':form_pais,
        }
    )
