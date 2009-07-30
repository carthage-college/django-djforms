from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import date_based, list_detail

from djforms.jobpost.forms import JobApplyForm, Post
from djforms.jobpost.models import Post

import datetime
import re

def data_entered(request):
    return render_to_response('jobpost/data_entered.html')

def post_list(request, page=0):
    """
    Post list

    Template: ``jobpost/post_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
    """
    return list_detail.object_list(
        request,
        queryset = Post.objects.filter(publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now()),
        paginate_by = 5,
        page = page,
    )

def post_detail(request, slug):
    """
    Post detail

    Templates: ``jobpost/post_detail.html``
    Context:
        object:
            the object to be detailed
        """
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = JobApplyForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.job = post
            job.save()
            return HttpResponseRedirect('/job/data_entered')
    else:
        form = JobApplyForm()
    return render_to_response("jobpost/post_detail.html", {'form':form,'post':post}, context_instance=RequestContext(request))

def post_create(request):
    """
    Post list

    Template: ``jobpost/add_form.html``
    Context:
    """
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/job/data_entered')
    else:
        form = Post()
    return render_to_response("jobpost/add_form.html", {'form':form}, context_instance=RequestContext(request))

def category_list(request, page=0):
    """
    Category list

    Template: ``blog/category_list.html``
    Context:
        object_list
            List of categories.
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
        """
    return list_detail.object_list(
        request,
        queryset = Category.objects.all(),
        template_name = 'jobpost/category_list.html',
        paginate_by = 20,
        page = page,
    )

def category_detail(request, slug, page=0):
    """
    Category detail
    
    Template: ``jobpost/category_detail.html``
    Context:
        object_list
            List of posts specific to the given category.
        category
            Given category.
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
    """
    try:
        category = Category.objects.get(slug__iexact=slug)
    except Category.DoesNotExist:
        raise Http404
  
    return list_detail.object_list(
        request,
        queryset = category.post_set.filter(publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now()),
        extra_context = { 'category': category },
        template_name = 'jobpost/category_detail.html',
        paginate_by = 5,
        page = page,
    )

# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""


def search(request, page=0):
    """
    Search for jobpost posts.
    
    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.
    
    Template: ``jobs/post_search.html``
    Context:
    object_list
        List of jobpost posts that match given search term(s).
    search_term
        Given search term.
    """
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
        search_term = '%s' % request.GET['q']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        if len(cleaned_search_term) != 0:
            post_list = Post.objects.filter(description__icontains=cleaned_search_term, publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now())
            context = { 'object_list': post_list, 
                        'search_term':search_term,}
            return render_to_response('jobpost/post_search.html', context, context_instance=RequestContext(request))
        else:
            message = 'Search term was too vague. Please try again.'
            context = { 'message':message }
            return render_to_response('jobpost/post_search.html', context, context_instance=RequestContext(request))
    else:
        return render_to_response('jobpost/post_search.html', {}, context_instance=RequestContext(request))
