from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

from djforms.giving.forms import *
from djforms.core.models import Promotion
from djforms.giving.models import PaverContact, DonationContact
from djforms.processors.forms import TrustCommerceForm as CreditCardForm

from djtools.fields import TODAY
from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta

import os
import json
import time

YEAR = TODAY.year
REQUIRED_ATTRIBUTE = settings.REQUIRED_ATTRIBUTE


def meme(img, draw, msg, pos):
    lines = []

    color = 'rgb(122,35,47)' # carthage red
    fontsize=250

    font = ImageFont.truetype(settings.GIVING_DAY_FONT, size=fontsize)
    w, h = draw.textsize(msg, font)

    imgWidthWithPadding = img.width * 0.99

    # 1. how many lines for the msg to fit ?
    lineCount = 1
    if(w > imgWidthWithPadding):
        lineCount = int(round((w / imgWidthWithPadding) + 1))

    if lineCount > 2:
        while 1:
            fontsize -= 2
            font = ImageFont.truetype(settings.GIVING_DAY_FONT, size=fontsize)
            w, h = draw.textsize(msg, font)
            lineCount = int(round((w / imgWidthWithPadding) + 1))
            if lineCount < 3 or fontsize < 10:
                break

    # 2. divide text in X lines
    lastCut = 0
    isLast = False
    for i in range(0,lineCount):
        if lastCut == 0:
            cut = (len(msg) / lineCount) * i
        else:
            cut = lastCut

        if i < lineCount-1:
            nextCut = (len(msg) / lineCount) * (i+1)
        else:
            nextCut = len(msg)
            isLast = True

        # make sure we don't cut words in half
        if nextCut == len(msg) or msg[nextCut] == " ":
            pass
        else:
            while msg[nextCut] != " ":
                nextCut += 1

        line = msg[cut:nextCut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not isLast and w > imgWidthWithPadding:
            nextCut -= 1
            while msg[nextCut] != " ":
                nextCut -= 1

        lastCut = nextCut
        lines.append(msg[cut:nextCut].strip())

    # 3. print each line centered
    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 10

    for i in range(0,lineCount):
        w, h = draw.textsize(lines[i], font)
        textX = img.width/2 - w/2
        textY = lastY + h
        draw.text((textX-2, textY-2),lines[i], fill=color, font=font)
        draw.text((textX+2, textY-2),lines[i], fill=color, font=font)
        draw.text((textX+2, textY+2),lines[i], fill=color, font=font)
        draw.text((textX-2, textY+2),lines[i], fill=color, font=font)
        draw.text((textX, textY),lines[i], fill=color, font=font)
        lastY = textY

    return img


def photo_caption(request):
    if request.POST:
        form = PhotoCaptionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            image = Image.open(settings.GIVING_DAY_CAPTION_FILE_ORIG)
            draw = ImageDraw.Draw(image)

            color = 'rgb(122,35,47)' # carthage red
            fontsize=250
            font = ImageFont.truetype(settings.GIVING_DAY_FONT, size=fontsize)

            caption1 = cd['caption1']
            caption2 = cd['caption2']
            caption3 = cd['caption3']
            (x, y) = (680, 1700)
            draw.text((x, y), caption1, fill=color, font=font)
            (x, y) = (685, 2020)
            draw.text((x, y), caption2, fill=color, font=font)
            (x, y) = (700, 2300)
            draw.text((x, y), caption3, fill=color, font=font)
            #image = meme(image, draw, caption1, 'top')
            image.save(settings.GIVING_DAY_CAPTION_FILE_NEW)
            foto = time.time()
    else:
        foto = False
        form = PhotoCaptionForm()
    return render(
        request, 'giving/manager/photo_caption.html', {
            'form':form,'foto':foto
        }
    )


def giving_form(request, transaction, campaign=None):
    """Multipurpose function to handle various types of donations."""
    if settings.DEBUG or not settings.TC_LIVE:
        bcc = settings.MANAGERS
    else:
        bcc = settings.GIVING_DONATIONS_BCC

    status = None
    trans_cap = transaction.capitalize()
    # check for a campaign and obtain contact form
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
        ct_form_name = '{0}{1}ContactForm'.format(
            campaign.slug.replace('-', ' ').title().replace(' ', ''),
            trans_cap,
        )
        or_form_name = '{0}{1}OrderForm'.format(
            campaign.slug.replace('-', ' ').title().replace(' ', ''),
            trans_cap,
        )
    else:
        campaign = ''
        ct_form_name = '{0}ContactForm'.format(trans_cap)
        # order form
        or_form_name = '{0}OrderForm'.format(trans_cap)

    or_form = str_to_class(
        'djforms.giving.forms', or_form_name,
    )
    ct_form = str_to_class(
        'djforms.giving.forms', ct_form_name,
    )

    # there might not be a custom campaign form
    # so we just use the default contact form
    if campaign and not ct_form:
        ct_form_name = '{0}{1}ContactForm'.format(
            settings.GIVING_DEFAULT_CONTACT_FORM,
            trans_cap,
        )
        ct_form = str_to_class(
            'djforms.giving.forms', ct_form_name,
        )
    if campaign and not or_form:
        or_form_name = 'DonationOrderForm'
        or_form = DonationOrderForm()

    years = None
    if request.POST:
        ct_form = str_to_class(
            'djforms.giving.forms', ct_form_name,
        )(request.POST, prefix='ct', use_required_attribute=REQUIRED_ATTRIBUTE)
        or_form = str_to_class(
            'djforms.giving.forms', or_form_name,
        )(request.POST, prefix='or', use_required_attribute=REQUIRED_ATTRIBUTE)
        cc_form = CreditCardForm(
            or_form,
            ct_form,
            request.POST,
            use_required_attribute=REQUIRED_ATTRIBUTE,
        )

        if ct_form.is_valid() and or_form.is_valid():
            contact = ct_form.save()
            or_data = or_form.save(commit=False)
            or_data.status = 'In Process'
            or_data.operator = 'DJForms{}'.format(trans_cap)
            or_data.avs = 0
            or_data.auth = 'sale'
            # deal with commemorative paver options
            class_of = contact.class_of
            # donation amount calculation for current students
            if not campaign and class_of == str(YEAR):
                if or_data.total == 250:
                    or_data.total = PAVER_TYPES[0][0]
                elif or_data.total == 500:
                    or_data.total = PAVER_TYPES[2][0]
                elif or_data.total == 1000:
                    or_data.total = PAVER_TYPES[4][0]

            if transaction == 'paver':
                comments = u'{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format(
                    ct_form['inscription_1'].value(),
                    ct_form['inscription_2'].value(),
                    ct_form['inscription_3'].value(),
                    ct_form['inscription_4'].value(),
                    ct_form['inscription_5'].value(),
                    ct_form['inscription_6'].value(),
                    ct_form['inscription_7'].value(),
                )
                or_data.comments = comments
            # deal with payments if they have chosen to pledge
            if transaction != 'paver' and request.POST.get('or-pledge') != '':
                or_data.payments = 0
                or_data.auth = 'store'
                or_data.cycle = '1m'
            else:
                or_data.payments = None
            if campaign:
                or_data.promotion = campaign
            or_data.save()
            contact.order.add(or_data)
            email = contact.email
            cc_form = CreditCardForm(
                or_data, contact, request.POST,
            )
            if cc_form.is_valid():
                # save and update order
                r = cc_form.processor_response
                or_data.status = r.msg['status']
                or_data.transid = r.msg['transid']
                or_data.billingid = r.msg.get('billingid')
                or_data.cc_name = cc_form.name
                or_data.cc_4_digits = cc_form.card[-4:]
                or_data.save()
                # sendmail
                or_data.contact = contact
                data = {'order': or_data, 'years': years}
                # subject of email
                SUBJECT = u"Thank you, {} {}{} for your donation to Carthage"
                try:
                    if contact.spouse:
                        spouse = ' and {0},'.format(contact.spouse)
                    else:
                        spouse = ','
                except Exception:
                    spouse = ''
                subject = SUBJECT.format(
                    contact.first_name, contact.last_name, spouse,
                )
                # build our email template path
                template = 'giving/{}_email.html'.format(transaction)
                if campaign:
                    temp = 'giving/campaigns/{0}/{1}_email.html'.format(
                        campaign.slug, transaction,
                    )
                    sendero = os.path.join(
                        settings.ROOT_DIR, 'templates', temp,
                    )
                    if os.path.isfile(sendero):
                        template = temp
                    else:
                        template = 'giving/campaigns/{0}/{1}_email.html'.format(
                            settings.GIVING_DEFAULT_CAMPAIGN, transaction,
                        )
                sent = send_mail(
                    request, [email], subject, email, template, data, bcc,
                )
                or_data.send_mail = sent
                or_data.save()
                # redirect
                if campaign:
                    url = reverse(
                        'giving_success_campaign',
                        args=[transaction,campaign.slug]
                    )
                else:
                    url = reverse(
                        'giving_success_generic',
                        args=[transaction]
                    )
                return HttpResponseRedirect(url)
            else:
                r = cc_form.processor_response
                if r:
                    or_data.status = r.status
                else:
                    or_data.status = 'Form Invalid'
                or_data.cc_name = cc_form.name
                if cc_form.card:
                    or_data.cc_4_digits = cc_form.card[-4:]
                status = or_data.status
                or_data.save()

    else:
        # order form
        init = {}
        if request.GET.get('amount'):
            try:
                # simple way to guard against malicious data
                init['total'] = '{0:.2f}'.format(
                    float(request.GET.get('amount'))
                )
            except:
                pass

        if campaign and campaign.designation:
            init['comments'] = campaign.designation

        or_form = str_to_class(
            'djforms.giving.forms', or_form_name
        )(prefix='or', initial=init, use_required_attribute=REQUIRED_ATTRIBUTE)

        # contact form
        ct_form = str_to_class(
            'djforms.giving.forms', ct_form_name
        )(prefix='ct', use_required_attribute=REQUIRED_ATTRIBUTE)
        # credit card
        cc_form = CreditCardForm(use_required_attribute=REQUIRED_ATTRIBUTE)

    # build our template path
    modal = ''
    if request.GET.get('modal'):
        modal = 'modal_'
    template = 'giving/{0}_{1}form.html'.format(transaction, modal)
    if campaign:
        temp = 'giving/campaigns/{0}/{1}_{2}form.html'.format(
            campaign.slug, transaction, modal,
        )
        if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', temp)):
            template = temp
        else:
            template = 'giving/campaigns/{0}/{1}_{2}form.html'.format(
                settings.GIVING_DEFAULT_CAMPAIGN, transaction, modal,
            )

    return render(
        request,
        template,
        {
            'ct_form': ct_form,
            'or_form': or_form,
            'form_proc': cc_form,
            'status': status,
            'campaign': campaign,
            'year': str(YEAR),
            'desi': [
                "Women 150 Scholarship Fund",
                "Women 150 Aspire/Professional Development Fund",
                "Women 150 Women's Athletics Fund",
            ],
        },
    )


def giving_success(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)

    # build our template path
    template = 'giving/{}_success.html'.format(transaction)
    if campaign:
        temp = 'giving/campaigns/{}/{}_success.html'.format(
            campaign.slug, transaction
        )
        if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', temp)):
            template = temp
        else:
            template = 'giving/campaigns/{}/{}_success.html'.format(
                settings.GIVING_DEFAULT_CAMPAIGN, transaction
            )

    return render(
        request, template, { 'campaign': campaign, }
    )


def donors(request, slug=None):

    promo = None
    percent = 0
    #start_date = TODAY - timedelta(days=365)
    start_date = TODAY - timedelta(days=300)
    template = 'giving/donors.html'

    if slug:
        promo = get_object_or_404(Promotion, slug=slug)
        if slug == 'giving-day':
            start_date = settings.GIVING_DAY_START_DATE

        percent = promo.percent()
        # template
        temp = 'giving/campaigns/{}/donors.html'.format(promo.slug)
        if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', temp)):
            template = temp

    donors = DonationContact.objects.filter(anonymous=False).filter(
        order__time_stamp__gte=start_date
    ).filter(order__status__in=['approved','manual'])


    if slug and slug != 'giving-day':
        donors = donors.filter(order__promotion__slug=slug)

    spouses = donors.filter(spouse_class__isnull=False).exclude(spouse_class=' ')
    #count = donors.count() + spouses.count()
    count = donors.count()
    ctext = {
        'donors':donors, 'promo':promo, 'count':count,
        'percent': percent, 'spouses':spouses
    }

    if request.GET.get('ajax'):
        response = render(
            request, 'giving/donors.json', ctext,
            content_type='text/plain; charset=utf-8'
        )
    elif request.GET.get('latest'):
        try:
            latest = int(request.GET.get('latest'))
            ctext['donors'] = donors.order_by('-order__time_stamp')[:latest]
            ctext['spouses'] = spouses.order_by('-order__time_stamp')[:latest]
            response = render(
                request, 'giving/donors_latest.html', ctext,
                content_type='text/plain; charset=utf-8'
            )
        except:
            raise Http404
    elif request.GET.get('relation'):
        donors = donors.filter(relation=request.GET.get('relation'))
        spouses = donors.filter(spouse_class__isnull=False).exclude(spouse_class=' ')
        count = donors.count() + spouses.count()
        results = [{"count": "{}".format(donors.count()),}]
        response = HttpResponse(
            json.dumps(results),
            content_type='application/json; charset=utf-8'
        )
    else:
        response = render(
            request, template, ctext
        )

    return response


def promotion_ajax(request, slug):
    """
    ajax request, returns HTML for dynamic display.
    accepts a campaign slug for identifying the Promotion() class object.
    """

    promo = get_object_or_404(Promotion, slug=slug)
    url = reverse('giving_form_campaign', args=['donation', slug])

    return render(
        request, 'giving/promotion_ajax.html',
        {'data':promo,'earl':url}
    )


@staff_member_required
def manager_cash(request):
    """
    cash donation form
    """

    if request.POST:
        ct_form = ManagerContactForm(request.POST, prefix='ct')
        or_form = ManagerOrderForm(request.POST, prefix='or')
        if ct_form.is_valid() and or_form.is_valid():
            # contact
            contact = ct_form.save(commit=False)
            contact.opt_in = 0
            contact.anonymous = 0
            contact.matching_company = 0
            contact.save()
            # order
            or_data = or_form.save(commit=False)
            or_data.status = 'Manual'
            or_data.operator = 'DJFormsCashDonation'
            or_data.avs = 0
            or_data.auth = 'cash'
            or_data.save()
            contact.order.add(or_data)
            # redirect
            return HttpResponseRedirect( reverse( 'giving_manager_success') )
    else:
        ct_form = ManagerContactForm(prefix='ct')
        or_form = ManagerOrderForm(prefix='or')

    return render(
        request, 'giving/manager/cash_form.html',
        {'ct_form': ct_form, 'or_form':or_form,}
    )


@staff_member_required
def manager(request, slug=None):
    """
    home view that displays all donors
    """

    promo = None
    start_date = TODAY - timedelta(days=365)
    end_date = TODAY + timedelta(days=1)

    if slug == 'paver':
        donors = PaverContact.objects.filter(
            order__time_stamp__gte=start_date
        ).filter(order__status__in=['approved','manual'])
    else:
        if slug:
            promo = get_object_or_404(Promotion, slug=slug)

            if slug == 'giving-day':
                start_date = settings.GIVING_DAY_START_DATE
                end_date = settings.GIVING_DAY_END_DATE

        donors = DonationContact.objects.filter(
            order__time_stamp__gte=start_date
        ).filter(
            order__time_stamp__lte=end_date
        ).filter(order__status__in=['approved','manual'])

        if slug and  slug != 'giving-day':
            donors = donors.filter(order__promotion__slug=slug)

    return render(
        request, 'giving/manager/home.html', {
            'objects':donors, 'count':donors.count(), 'campaign':promo,
            'slug':slug
        }
    )
