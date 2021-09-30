from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from djforms.polisci.mun.forms import AttenderForm, CountryForm

from djtools.utils.mail import send_mail


def registration(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = settings.POLISCI_MODEL_UN_TO_LIST

    BCC = settings.MANAGERS

    if request.method == 'POST':
        form_cont = AttenderForm(request.POST, prefix='cont', label_suffix='')
        form_pais = CountryForm(request.POST, prefix='pais')
        if form_cont.is_valid() and form_pais.is_valid():
            contact = form_cont.cleaned_data
            data = {'object':contact,'dele':form_pais.cleaned_data}
            subject = "[Model United Nations Registration] {} {} of {}".format(
                contact['first_name'], contact['last_name'],
                contact['school_name']
            )
            send_mail(
                request, TO_LIST, subject, contact['email'],
                'polisci/mun/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('model_united_nations_success')
            )
    else:
        form_cont = AttenderForm(prefix='cont', label_suffix='')
        form_pais = CountryForm(prefix='pais')

    return render(
        request, 'polisci/mun/form.html',
        {'form_cont':form_cont,'form_pais':form_pais}
    )
