# -*- coding: utf-8 -*-

import os
import json
import time

from datetime import timedelta
from datetime import date
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models.query import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djforms.giving.forms import *
from djforms.core.models import Promotion
from djforms.giving.models import DonationContact
from djforms.giving.models import PaverContact
from djforms.processors.forms import TrustCommerceForm as CreditCardForm
from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class
from PIL import Image, ImageDraw, ImageFont


REQUIRED_ATTRIBUTE = settings.REQUIRED_ATTRIBUTE


def meme(img, draw, msg, pos):
    lines = []

    color = 'rgb(122, 35, 47)' # carthage red
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
    for i in range(0, lineCount):
        if lastCut == 0:
            cut = (len(msg) / lineCount) * i
        else:
            cut = lastCut

        if i < lineCount-1:
            nextCut = (len(msg) / lineCount) * (i + 1)
        else:
            nextCut = len(msg)
            isLast = True

        # make sure we don't cut words in half
        if nextCut == len(msg) or msg[nextCut] == ' ':
            pass
        else:
            while msg[nextCut] != ' ':
                nextCut += 1

        line = msg[cut:nextCut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not isLast and w > imgWidthWithPadding:
            nextCut -= 1
            while msg[nextCut] != ' ':
                nextCut -= 1

        lastCut = nextCut
        lines.append(msg[cut:nextCut].strip())

    # 3. print each line centered
    lastY = -h
    if pos == 'bottom':
        lastY = img.height - h * (lineCount + 1) - 10

    for i in range(0, lineCount):
        w, h = draw.textsize(lines[i], font)
        textX = img.width / 2 - w / 2
        textY = lastY + h
        draw.text((textX - 2, textY - 2),lines[i], fill=color, font=font)
        draw.text((textX + 2, textY - 2),lines[i], fill=color, font=font)
        draw.text((textX + 2, textY + 2),lines[i], fill=color, font=font)
        draw.text((textX - 2, textY + 2),lines[i], fill=color, font=font)
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

            color = 'rgb(122, 35, 47)' # carthage red
            fontsize = 250
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
        request,
        'giving/manager/photo_caption.html',
        {'form': form, 'foto': foto},
    )


def giving_form(request, transaction, campaign=None):
    """Multipurpose function to handle various types of donations."""
    if settings.DEBUG or not settings.TC_LIVE:
        bcc = settings.MANAGERS
    else:
        bcc = settings.GIVING_DONATIONS_BCC

    year = date.today().year
    if date.today().month >= 9:
        year += 1
    status = None
    trans_cap = transaction.capitalize()
    # might be a modal windows
    modal = request.GET.get('modal', '')
    if modal:
        modal = 'modal_'
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

    or_form = str_to_class('djforms.giving.forms', or_form_name)
    ct_form = str_to_class('djforms.giving.forms', ct_form_name)

    # there might not be a custom campaign form
    # so we just use the default contact form
    if campaign and not ct_form:
        ct_form_name = '{0}{1}ContactForm'.format(
            settings.GIVING_DEFAULT_CONTACT_FORM,
            trans_cap,
        )
        ct_form = str_to_class('djforms.giving.forms', ct_form_name)
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
            or_data.operator = 'DJForms{0}'.format(trans_cap)
            or_data.avs = 0
            or_data.auth = 'sale'
            # deal with commemorative paver options
            class_of = contact.class_of
            # donation amount calculation for current students
            if not campaign and class_of == str(year):
                if or_data.total == 250:
                    or_data.total = PAVER_TYPES[0][0]
                elif or_data.total == 500:
                    or_data.total = PAVER_TYPES[2][0]
                elif or_data.total == 1000:
                    or_data.total = PAVER_TYPES[4][0]

            if transaction == 'paver':
                comments = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format(
                    ct_form['inscription_1'].value(),
                    ct_form['inscription_2'].value(),
                    ct_form['inscription_3'].value(),
                    ct_form['inscription_4'].value(),
                    ct_form['inscription_5'].value(),
                    ct_form['inscription_6'].value(),
                    ct_form['inscription_7'].value(),
                )
                or_data.comments = comments
            elif or_form['comments_other']:
                or_data.comments = or_form['comments_other'].value()
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
            cc_form = CreditCardForm(or_data, contact, request.POST)
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
                subject = 'Thank you, {0} {1}{2} for your donation to Carthage'
                try:
                    if contact.spouse:
                        spouse = ' and {0},'.format(contact.spouse)
                    else:
                        spouse = ','
                except Exception:
                    spouse = ''
                subject = subject.format(contact.first_name, contact.last_name, spouse)
                # build our email template path
                template = 'giving/{0}_email.html'.format(transaction)
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
                if modal:
                    modal = '?modal={0}'.format(modal)
                if campaign:
                    url = '{0}{1}'.format(
                        reverse(
                            'giving_success_campaign',
                            args=[transaction, campaign.slug],
                        ),
                        modal,
                    )
                else:
                    url = '{0}{1}'.format(
                        reverse('giving_success_generic', args=[transaction]),
                        modal,
                    )
                return HttpResponseRedirect(url)
            else:
                resp = cc_form.processor_response
                if resp:
                    or_data.status = resp.status
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
            except Exception:
                pass

        or_form = str_to_class(
            'djforms.giving.forms', or_form_name,
        )(prefix='or', initial=init, use_required_attribute=REQUIRED_ATTRIBUTE)

        # contact form
        ct_form = str_to_class(
            'djforms.giving.forms', ct_form_name,
        )(prefix='ct', use_required_attribute=REQUIRED_ATTRIBUTE)
        # credit card
        cc_form = CreditCardForm(use_required_attribute=REQUIRED_ATTRIBUTE)

    # build our template path
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
            'year': str(year),
        },
    )


def giving_success(request, transaction, campaign=None):
    """Dispaly succes page after submitting a donation for a campaign."""
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
    # might be a modal windows
    modal = request.GET.get('modal', '')
    if modal:
        modal = 'modal_'

    # build our template path
    template = 'giving/{0}_{1}success.html'.format(transaction, modal)
    if campaign:
        temp = 'giving/campaigns/{0}/{1}_{2}success.html'.format(
            campaign.slug, transaction, modal,
        )
        if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', temp)):
            template = temp
        else:
            template = 'giving/campaigns/{0}/{1}_{2}success.html'.format(
                settings.GIVING_DEFAULT_CAMPAIGN, transaction, modal,
            )

    return render(request, template, {'campaign': campaign})


def donors(request, slug=None):
    """Display the donors to a campaign or default donation."""
    promo = None
    percent = 0
    date_start = date.today() - timedelta(days=365)
    date_end = date.today() + timedelta(days=1)

    template = 'giving/donors.html'
    relation = request.GET.get('relation')
    latest = request.GET.get('latest')
    if slug:
        promo = get_object_or_404(Promotion, slug=slug)

        percent = promo.percent()
        # template
        temp = 'giving/campaigns/{0}/donors.html'.format(promo.slug)
        if os.path.isfile(os.path.join(settings.ROOT_DIR, 'templates', temp)):
            template = temp
        if slug == 'giving-day':
            date_start = settings.GIVING_DAY_START_DATE
            date_end = settings.GIVING_DAY_END_DATE
            slug = None

    donations = DonationContact.objects.filter(anonymous=False).filter(
        created_at__range=(date_start, date_end),
    ).filter(hidden=False)

    if latest:
        latest = int(latest)
        donations = donations.order_by('-created_at')
    else:
        donations = donations.order_by('last_name')

    if relation:
        donations = donations.filter(relation=relation)

    donors = []
    donors_promo = []
    for donor in donations:
        if donor.order_status() in {'approved', 'manual'}:
            spouse = donor.spouse
            donor_dict = {
                'last_name': donor.last_name,
                'first_name': donor.first_name,
                'class_of': donor.class_of,
                'relation': donor.relation,
                'spouse': donor.spouse,
            }
            if slug and donor.order_promo() and donor.order_promo().slug==slug:
                donors_promo.append(donor_dict)
            else:
                donors.append(donor_dict)
    if slug:
        donors = donors_promo

    if latest:
        donors = donors[:latest]

    ctext = {
        'donors': donors,
        'promo': promo,
        'count': len(donors),
        'percent': percent,
    }

    if request.GET.get('ajax'):
        response = render(
            request,
            'giving/donors.json',
            ctext,
            content_type='text/plain; charset=utf-8',
        )
    elif latest:
        response = render(
            request,
            'giving/donors_latest.html',
            ctext,
            content_type='text/plain; charset=utf-8',
        )
    elif relation:
        results = [{"count": "{0}".format(ctext['count'])}]
        response = HttpResponse(
            json.dumps(results),
            content_type='application/json; charset=utf-8',
        )
    else:
        response = render(request, template, ctext)

    return response


def promotion_ajax(request, slug):
    """
    ajax request, returns HTML for dynamic display.
    accepts a campaign slug for identifying the Promotion() class object.
    """

    promo = get_object_or_404(Promotion, slug=slug)
    url = reverse('giving_form_campaign', args=['donation', slug])

    return render(
        request,
        'giving/promotion_ajax.html',
        {'data': promo, 'earl': url},
    )


@staff_member_required
def manager_cash(request):
    """Cash donation form."""
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
            return HttpResponseRedirect(reverse('giving_manager_success'))
    else:
        ct_form = ManagerContactForm(prefix='ct')
        or_form = ManagerOrderForm(prefix='or')

    return render(
        request,
        'giving/manager/cash_form.html',
        {'ct_form': ct_form, 'or_form': or_form},
    )


@csrf_exempt
@staff_member_required
def manager_ajax(request):
    """ajax response for dashboard home for managers."""
    donations = None
    post = request.POST
    # draw counter
    draw = int(post.get('draw', 0))
    # paging first record indicator.
    start = int(post.get('start', 0))
    # number of records that the table can display in the current draw
    length = int(post.get('length', 100))
    # page number, 1-based index
    page = int((start / length) + 1)
    # search box data
    search = post.get('search[value]')
    # order by
    order_by = '-created_at'
    order = post.get('order[0][column]')
    if order:
        order = int(order)
        # column names
        columns = DonationContact.COLUMNS
        # direction
        dirx = post.get('order[0][dir]')
        col = columns.get(order)
        order_by = col if dirx == 'asc' else '-' + col
    date_start = date.today() - timedelta(days=365)
    date_end = date.today() + timedelta(days=1)
    group = request.POST.get('group', None)

    all_donations = DonationContact.objects.filter(
        created_at__gte=date_start,
    ).filter(
        created_at__lte=date_end,
    )
    if search:
        donations = all_donations.filter(
            Q(last_name__icontains=search)|
            Q(first_name__icontains=search)
        )
    else:
        donations = all_donations.order_by(order_by)
    records_total = donations.count()
    records_filtered = records_total
    paginator = Paginator(donations, length)
    object_list = paginator.page(page).object_list
    data = []
    for donor in object_list:
        if donor.order_status() in {'approved', 'manual'}:
            promo = donor.order_promo()
            if promo:
                promo = promo.title
            spouse = ''
            if donor.spouse:
                spouse = '{0} {1}'.format(donor.spouse, donor.spouse_class or '')
            address = '{0} {1}'.format(donor.address1, donor.address2 or '')
            last_name = '<a href="{0}" target="_blank">{1}</a>'.format(
                reverse(
                    'admin:giving_donationcontact_change', args=(donor.id,),
                ),
                donor.last_name,
            )
            created_at = '<a href="{0}" target="_blank">{1}</a>'.format(
                reverse(
                    'admin:processors_order_change', args=(donor.order_oid(),),
                ),
                donor.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            )
            data.append({
                'last_name': last_name,
                'first_name': donor.first_name,
                'order_cc_name': donor.order_cc_name(),
                'created_at': created_at,
                'email': donor.email,
                'twitter': donor.twitter or '',
                'phone': donor.phone or '',
                'address': address,
                'city': donor.city or '',
                'state': donor.state or '',
                'postal_code': donor.postal_code or '',
                'spouse': spouse,
                'relation': donor.relation or '',
                'honouring': donor.honouring or '',
                'class_of': donor.class_of or '',
                'order_promo': promo or '',
                'order_transid': donor.order_transid(),
                'order_status': donor.order_status(),
                'order_total': donor.order_total(),
                'order_comments': donor.order_comments(),
                'anonymous': donor.anonymous,
                'hidden': donor.hidden,
            })

    return JsonResponse(
        {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        },
        safe=False,
    )


@staff_member_required
def manager(request, slug=None):
    """Home view that displays all donors."""
    return render(request, 'giving/manager/home.html', {})
