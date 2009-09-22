# -*- coding: utf-8 -*-

import logging
from django.core.mail import send_mail
from django.db import models, connection
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template import Context, loader
from djforms.contact.conf import settings

logger = logging.getLogger('models')


class Message(models.Model):
    """
    A message received by way of the contact form.
    The "sent" field indicates if the mail was sent or not.
    """
    name = models.CharField(_('name'), max_length=80)
    mail = models.EmailField(_('email'))
    subject = models.CharField(_('subject'), max_length=256, blank=True)
    message = models.TextField(_('message'))
    sent = models.BooleanField(_('is sent'), default=False)

    def __unicode__(self):
        fromdata = {'name': self.name, 'mail': self.mail}
        return _('message from %(name)s (%(mail)s)') % fromdata

    def render_message(self, template_name=settings.DEFAULT_TEMPLATE):
        context = Context({'name': self.name,
                           'mail': self.mail,
                           'message': self.message})
        return mark_safe(loader.render_to_string(template_name, context))

    def send(self, slug, fail_silently=False, extra_recipients=[]):
        """
        Attempt to send the message by mail to the users with permission
        to receive contact messages and to those recipients who appear in
        the 'extra_recipients' list.
        The message is sent via the template
        In the event that the message fails, an smtplib.SMTPException is
        thrown, unless 'fail_silently' is set to False.
        In any event, the message is saved in the database.
        """

        from_email = self.mail
        m = _('contact message will be sent from %(from_email)s') % {
                                                    'from_email': self.mail}
        logger.debug(m)
        #Grabs the proper id based on the slug
        #Checks the id against each user's group id
        #and sends out the mail to the proper users
        group_to_be_mailed = slug
        cursor = connection.cursor()

        query ="""SELECT u.email
            FROM %s a, %s g, %s u
            WHERE a.name = '%s'
            AND a.id = g.group_id
            AND g.user_id = u.id""" % ('auth_group', 'auth_user_groups', 'auth_user', group_to_be_mailed)
        cursor.execute(query)

        rcpt_list = [row[0] for row in cursor.fetchall()]
        rcpt_list += extra_recipients
        if not rcpt_list:
            self.sent = False
            m = _('could not find any recipients')
            logger.debug(m)
            if not fail_silently:
                raise ValueError(m)
        else:
            m = _('attempting to send "%(subject)s" to %(recipients)s' % {
                            'subject': self.subject, 'recipients': rcpt_list})
            logger.debug(m)
            # Enviamos el mensaje del formulario de contacto por mail a los
            # destinatarios.
            send_mail(self.subject,
                      self.render_message(),
                      from_email,
                      rcpt_list,
                      fail_silently)
            logger.debug(_('message sent'))
            self.sent = True

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')
        permissions = ('can_receive_messages', _('can receive messages')),
