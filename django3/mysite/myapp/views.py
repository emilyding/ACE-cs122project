'''
This file writes views. It uses render to pass in context and html templates to generate pages. Code for generating views of forms references https://www.pydanny.com/core-concepts-django-modelforms.html.
'''

#imports render and 404 errors
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import Http404

#imports forms and models
from django import forms
from .models import Comment, Compare, Cuisine
from myapp.forms import MyCommentForm, MyCompareForm, MyCuisineForm
from django.utils import timezone 

#imports functions to interact with backend 
from yelp_sql_nograph import get_top_cuisines, price_ratings, star_reviews, common_cuisines, get_top_cities
from city_summary_stats import get_summary_info
from yelp_all_cities import cuisine_highlights
from compare_cities import compare_cuisines


def index(request):
    #view for homepage
    return render_to_response('index.html')

def about(request):
    #view for about page
    return render_to_response('about.html')

def overview(request):
    # view for overview page. (all city data)
    # get_summary_info generates fun facts from al cities data 
    data_info = get_summary_info({})
    facts = []
    for data in data_info:
        entry = [str(data[0]), str(data[1])]
        facts.append(entry)
    return render_to_response('overview.html',{"facts": facts})


def form(request): 
    # view for city snapshot input form. Reference link cited above.
    # uses MyCommentForm
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

def compare(request):
    # view for compare cities input form. Reference link cited above.
    # uses MyCompareForm
    if request.method == "POST":
        form = MyCompareForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/cresults')
    else:
        form = MyCompareForm()
        return render(request, "compare.html", {'form': form})

def cuisine(request):
    # view for cuisine input form. Reference link cited above.
    # uses MyCuisineForm
    if request.method == "POST":
        form = MyCuisineForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/cuiresults')
    else:
        form = MyCuisineForm()
        return render(request, "cuisine.html", {'form': form}) 

def cuiresults(request):
    # cuisine results after cuisine form is submitted.
    # Cuisine objects referenced by id (most recent is also length of objects.all())
    num = len(Cuisine.objects.all())
    last_entry = get_object_or_404(Cuisine, pk = num)
    cuisine = last_entry.make_dict()
    #get_top_cities returns top cities given cuisine. Limit set at 10
    top_cities = get_top_cities({"cuisine": cuisine, "limit":10})
    #convert data into input for google charts
    bar1 = [[x[0], x[1]] for x in top_cities]
    bar2 = [[x[0], x[2]] for x in top_cities]
    return render(request, 'cuiresults.html', {'cuisine': cuisine, 'bar1': bar1, 'bar2': bar2})


def cresults(request):
    # Compare objects referenced by id (most recent is also length of objects.all())
    num = len(Compare.objects.all())
    last_entry = get_object_or_404(Compare, pk = num)
    args = last_entry.make_dict()
    #compare_cuisines with two cities
    list_difference = compare_cuisines(args[0], args[1])
    list_difference.sort(key = lambda x: x[3], reverse = True)
    
    #generate input for google chart
    cuisine_comparison = []
    for entry in list_difference:
        if entry[0] == args[2]:
            cuisine_comparison = [[args[0]['city'], entry[1]], [args[1]['city'], entry[2]]]
    places_to_go_city1 = list_difference[:9]
    places_to_go_city2 = list_difference[-10:]
    bar1 = [[x[0], x[1], x[2]] for x in places_to_go_city1]
    bar2 = [[x[0], x[1], x[2]] for x in places_to_go_city2]

    return render(request, 'cresults.html', {'city1': str(args[0]['city']), 'city2': str(args[1]['city']), 'bar1': bar1, 'bar2': bar2, 'cuisine': args[2], 'comparison': cuisine_comparison})

def results(request):
    # city snapshot results after /form is submitted.
    # Cuisine objects referenced by id (most recent is also length of objects.all())
    num = len(Comment.objects.all())
    latest_city = get_object_or_404(Comment, pk = num )
    args = latest_city.make_dict()
    #formatting of argument to use yelp_nograph functions
    if args["worst"] == "Best":
        bw = "Best"
        args["worst"] = False
    else:
        bw = "Worst"
        args["worst"] = True

    # originally for num_limit field, but removed
    #if args["limit"] == "All":
    #    args.pop("limit")
    #else:

    # limit best/worst results to 10
    args["limit"] = 10

    #get fun facts summary info
    query = {"city": args['city']}
    info = []
    data_info = get_summary_info(query)
    for data in data_info:
        entry = [str(data[0]), str(data[1])]
        info.append(entry)
    
    #top cuisine in a city
    top_cuisines = get_top_cuisines(args)
    #data_barstop = top_cuisines[0:5]
    barstop = []
    for data in top_cuisines:
        entry = [data[0], data[2]]
        barstop.append(entry)

    # price data
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

    #stars data
    data_stars = star_reviews(query)
    piestar = []
    linestar = []
    for data in data_stars:
        entrypie = [str(data[0]), data[1]]
        entryline = [str(data[0]), data[2]]
        piestar.append(entrypie)
        linestar.append(entryline)

    #common cuisines data
    barcommon = []
    topcommon, data_common = common_cuisines(query)
    for top in topcommon:
        entry = [top[0], top[2]]
        barcommon.append(entry)

    return render(request, 'charts.html', {'best_worst': bw, 'plt1_bar':barstop,'title': args['city'], 
        "plt2_pie":pieprice, "plt3_line":lineprice, "plt4_line":linenumperres,"plt5_pie":piestar, "plt6_line":linestar, 
        "plt7_bar": barcommon, "plt8_scatter": data_common, "info": info})

def top_cuisines(request):
    # generates view for top_cuisines
    return render_to_response('top_cuisines.html')
