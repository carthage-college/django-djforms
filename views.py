from django.shortcuts import render_to_response

def request_complete(request):
    return render_to_response('request_complete.html')
