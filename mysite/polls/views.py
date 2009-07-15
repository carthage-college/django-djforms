from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mysite.polls.models import Choice, Poll
#...
def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
	    selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
	    # Redisplay the poll voting form. 
            return render_to_response('polls/poll_detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
	    })
        else:
	    selected_choice.votes += 1
	    selected_choice.save()
	    #Always return an HttpResponseRedirect after successfully dealing
	    #with POST data. This prevents data from being posted twice if a 
	    #user hits the Back button. 
            return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

#return HttpResponseRedirect(reverse('mysite.polls.views.results', args=(p.id,)))

"""def results(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('polls/results.html', {'poll': p})

def index(request):
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	return render_to_response('polls/poll_list.html', {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('polls/poll_detail.html', {'poll': p})"""
