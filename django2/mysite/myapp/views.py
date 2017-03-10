from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Question, Comment
from django.http import Http404
from django import forms 
from yelp_sql import get_top_cuisines 
 
def index(request):
    return render_to_response('index.html')

def citylist(request):
    return render_to_response('citylist.html')

def about(request):
    return render_to_response('about.html')

def overview(request):
    return render_to_response('overview.html')

def detail(request):
    city = get_object_or_404(Question, pk=2)
    price_limit = get_object_or_404(Question, pk=3)
    num_results = get_object_or_404(Question, pk=4)
    best_worst = get_object_or_404(Question, pk=5)
    return render(request, 'detail.html', {'city': city, 'price_limit': price_limit, 'num_results':num_results, 'best_worst': best_worst})


from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from myapp.forms import MyCommentForm
import json

def name(request):
 
    if request.method == "POST":
        form = MyCommentForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/results')
 
    else:
 
        form = MyCommentForm()
 
        return render(request, "name.html", {'form': form})

def results(request):
    num = len(Comment.objects.all())
    latest_city = get_object_or_404(Comment, pk = num )
    args = latest_city.make_dict()
    if args["worst"] == "Best":
        args["worst"] = False
    else:
        args["worst"] = True
    if args["limit"] == "All":
        args.pop("limit")
    else:
        args["limit"] = int(args["limit"])

    top_cuisines = get_top_cuisines(args)[1]
    
    
    data_plot = top_cuisines[0:5]

    rows = []
    for data in data_plot:
        entry = [data[0], data[2]]
        rows.append(entry)
    


    #x = h(args)
    return render(request, 'charts.html', {'rows':rows, 'title': args['city']})

