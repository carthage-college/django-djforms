from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from djforms.communications.print.forms import RequestForm
from djtools.utils.mail import send_mail

