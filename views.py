from django.shortcuts import render_to_response

def reserve_complete(request):
    return render_to_response('reserve_thanks.html')