from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponseRedirect
from django.views.generic import date_based, list_detail
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from djforms.jobpost.forms import JobApplyForms, PostFormWithHidden, PostFormWithoutHidden, PostFormMostHidden
from djforms.jobpost.models import Post, Department, JobApplyForm
from django.contrib.auth.models import User

from dateutil import parser
import datetime
import re

@login_required
def data_entered(request):
    return render_to_response('jobpost/data_entered.html', context_instance=RequestContext(request))

@login_required
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
        queryset = Post.objects.filter(publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now(), active=1),
        paginate_by = 5,
        page = page,
    )

@staff_member_required
def user_post_list(request, page=0):
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
    current_user = request.user
    return list_detail.object_list(
        request,
        queryset = Post.objects.filter(creator = current_user),
        template_name = 'jobpost/user_post_list.html',
        paginate_by = 5,
        page = page,
    )

@login_required
def post_detail(request, slug, page=0):
    """
    Post detail

    Templates: ``jobpost/post_detail.html``
    Context:
        object:
            the object to be detailed
        """
    #if the user is staff they see the applicants, and if they are the creator they can expire the post
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_staff:
        if post.creator==request.user:
            if request.method == 'POST':
                form = PostFormMostHidden(request.POST, instance=post)
                if form.is_valid():
                    post.num_positions = request.POST['num_positions']
                    post.expire_date = parser.parse(request.POST['expire_date'])
                    post.save()
                    return HttpResponseRedirect('/forms/job/data_entered')
            else:
                form = PostFormMostHidden(instance=post)
            return list_detail.object_list(
                request,
                queryset = JobApplyForm.objects.filter(job=post),
                template_name = 'jobpost/post_detail.html',
                paginate_by = 5,
                page = page,
                extra_context = {'post':post, "form": form},
            )
        else:
            return list_detail.object_list(
                request,
                queryset = JobApplyForm.objects.filter(job=post),
                template_name = 'jobpost/post_detail.html',
                paginate_by = 5,
                page = page,
                extra_context = {'post':post},
            )
    else:
        if request.method == 'POST':
            form = JobApplyForms(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.job = post
                data = job.save()
                form.save_m2m()
                t = loader.get_template('jobpost/email.txt')
                c = Context({'data':job,'post':post})
                email = EmailMessage((post.title + " application"), t.render(c), request.user.email, [post.creator.email], headers = {'Reply-To': request.user.email,'From': request.user.email})
                email.send(fail_silently=False)
                return HttpResponseRedirect('/forms/job/data_entered')
        else:
            form = JobApplyForms()
        return render_to_response("jobpost/post_detail.html", {'form':form,'post':post}, context_instance=RequestContext(request))

@permission_required('jobpost.can_manage', login_url= '/forms/job/data_entered/')
def post_manage(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostFormWithoutHidden(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/forms/job/data_entered')
    else:
        form = PostFormWithoutHidden(instance=post)
    return render_to_response("jobpost/post_manage.html", {"form": form,'original': post}, context_instance=RequestContext(request))
@permission_required('jobpost.can_manage', login_url= '/forms/job/data_entered/')
def post_manage_list(request, page=0):
    """
    Post list
    
    Template: ``jobpost/post_manage_list.html``
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
        #queryset = Post.objects.filter(publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now()),
        queryset = Post.objects.all(),
        paginate_by = 5,
        template_name = 'jobpost/post_manage_list.html',
        page = page,
    )

@staff_member_required
def post_create(request):
    """
    Post list

    Template: ``jobpost/add_form.html``
    Context:
    """
    
    if request.method == 'POST':
        form = PostFormWithHidden(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.creator = request.user
            data = new_post.save()
            form.save_m2m()
            t = loader.get_template('jobpost/post_created_email.txt')
            c = Context({'data':new_post,})
            #send_mail("New Job Post Created", t.render(c),"webmaster", ["skirk@carthage.edu",], fail_silently=False)
            send_mail("New Job Post Created", t.render(c),"Jennifer Rhyner", ["jrhyner@carthage.edu",], fail_silently=False)
            return HttpResponseRedirect('/forms/job/data_entered')
    else:
        form = PostFormWithHidden()
    return render_to_response("jobpost/add_form.html", {'form':form}, context_instance=RequestContext(request))

@login_required
def department_list(request, page=0):
    """
    Department list

    Template: ``blog/department_list.html``
    Context:
        object_list
            List of departments.
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
        queryset = Department.objects.all(),
        template_name = 'jobpost/department_list.html',
        paginate_by = 20,
        page = page,
    )

@login_required
def department_detail(request, slug, page=0):
    """
    Department detail
    
    Template: ``jobpost/department_detail.html``
    Context:
        object_list
            List of posts specific to the given department.
        department
            Given department.
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
        department = Department.objects.get(slug__iexact=slug)
    except Department.DoesNotExist:
        raise Http404
  
    return list_detail.object_list(
        request,
        queryset = department.post_set.filter(publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now(), active=1),
        extra_context = { 'department': department },
        template_name = 'jobpost/department_detail.html',
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

@login_required
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
            return list_detail.object_list(
                request,
                queryset = Post.objects.filter(description__icontains=cleaned_search_term, publish__lte=datetime.datetime.now(), expire_date__gte=datetime.datetime.now(), active=1),
                #extra_context = {'search_term':search_term},
                template_name="jobpost/post_search.html", 
                paginate_by=5,
                page = page,
            )
        else:
            message = 'Search term was too vague. Please try again.'
            context = { 'message':message }
            return render_to_response('jobpost/post_search.html', context, context_instance=RequestContext(request))
    else:
        return render_to_response('jobpost/post_search.html', {}, context_instance=RequestContext(request))
