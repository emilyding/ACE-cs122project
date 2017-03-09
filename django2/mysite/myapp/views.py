from django.shortcuts import render, render_to_response

def index(request):
    return render_to_response('index.html')

def citylist(request):
    return render_to_response('citylist.html')

def about(request):
    return render_to_response('about.html')

def overview(request):
    return render_to_response('overview.html')
