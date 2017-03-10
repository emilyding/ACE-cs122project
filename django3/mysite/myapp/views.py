from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Question, Comment
from django.http import Http404
from django import forms 
from yelp_sql_nograph import get_top_cuisines, price_ratings, star_ratings
from city_summary_stats import get_summary_info
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from myapp.forms import MyCommentForm
from yelp_all_cities import cuisine_highlights
import json

def index(request):
    return render_to_response('index.html')

def about(request):
    return render_to_response('about.html')

def overview(request):
    data_info = get_summary_info({})
    facts = []
    for data in data_info:
        entry = [str(data[0]), str(data[1])]
        facts.append(entry)
    return render_to_response('overview.html',{"facts": facts})

def form(request):
 
    if request.method == "POST":
        form = MyCommentForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/results')
 
    else:
 
        form = MyCommentForm()
 
        return render(request, "form.html", {'form': form})

def results(request):
    num = len(Comment.objects.all())
    latest_city = get_object_or_404(Comment, pk = num )
    args = latest_city.make_dict()
    if args["worst"] == "Best":
        bw = "Best"
        args["worst"] = False
    else:
        bw = "Worst"
        args["worst"] = True
    if args["limit"] == "All":
        args.pop("limit")
    else:
        args["limit"] = int(args["limit"])
    #get summary info

    query = {"city": args['city']}
    info = []
    data_info = get_summary_info(query)
    for data in data_info:
        entry = [str(data[0]), str(data[1])]
        info.append(entry)
    #compare to national average

    #top cuisine in a city
    top_cuisines = get_top_cuisines(args)
    data_barstop = top_cuisines[0:5]
    barstop = []
    for data in data_barstop:
        entry = [data[0], data[2]]
        barstop.append(entry)

    # price bracket
    data_price = price_ratings(query)
    pieprice = []
    lineprice = []
    linenumperres = []
    for data in data_price:
        entrypie = [data[0], data[2]]
        entryline = [data[0], data[1]]
        entrynumperres = [data[0], data[3]]
        pieprice.append(entrypie)
        lineprice.append(entryline)
        linenumperres.append(entrynumperres)

    #stars
    data_stars = star_ratings(query)
    piestar = []
    linestar = []
    for data in data_stars:
        entrypie = [str(data[0]), data[1]]
        entryline = [str(data[0]), data[2]]
        piestar.append(entrypie)
        linestar.append(entryline)
    #x = h(args)
    return render(request, 'charts.html', {'best_worst': bw, 'plt1_bar':barstop,'title': args['city'], 
        "plt2_pie":pieprice, "plt3_line":lineprice, "plt4_line":linenumperres,"plt5_pie":piestar, "plt6_line":linestar, "info": info})

def top_cuisines(request):
    
    return render_to_response('top_cuisines.html')
