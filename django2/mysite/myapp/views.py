from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Question, Comment
from django.http import Http404
from django import forms 
#
from myapp.somebsfunctions import hash_ as h

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
    x = h(args)
    return render(request, 'results.html', {'output': x})


# Create your views here.

from io import StringIO
from django.http import HttpResponse
from django.shortcuts import render_to_response
import pycha
import cairo

XML_PREAMBLE = '<?xml version="1.0" encoding="UTF-8"?>'

def colors_chart(inline = False):
    """
    Generate colours chart

    Set inline to True to disable the XML preamble
    """
    in_req = 1

    svg_buffer = StringIO()

    width, height = (500, 400)
    surface = cairo.SVGSurface(svg_buffer, width, height)

    dataSet = (
     ('dataSet 1', ((0, 1), (1, 3), (2, 2.5))),
     ('dataSet 2', ((0, 2), (1, 4), (2, 3))),
     ('dataSet 3', ((0, 5), (1, 1), (2, 0.5))),
    )

    options = {
        'legend': {'hide': True},
        'background': {'color': '#f0f0f0'},
        'colorScheme': {'name': 'fixed','args': {'colors': ['#ff0000', '#00ff00'],},
        },
        }

    import pycha.bar
    chart = pycha.bar.VerticalBarChart(surface, options)

    #import pycha.line
    #chart = pycha.line.LineChart(surface, options)
    chart.addDataset(dataSet)
    chart.render()

    del chart
    del surface

    response = ''

    if inline:
        svg_buffer.seek(len(XML_PREAMBLE))
    else:
        svg_buffer.seek(0)
    return svg_buffer.read()

def colors_svg(request):
    """ render a pure SVG chart """
    response = HttpResponse(mimetype='image/svg+xml')
    response.write(colors_chart(inline = False))
    return response

def chart(request):
    """ render a chart into the template """
    chart_svg = colors_chart(inline = True)

    return render_to_response(
        'charts.html',
        { "chart" : chart_svg },
        mimetype='application/xhtml+xml')