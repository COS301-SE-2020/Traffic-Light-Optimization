# Headers ................
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator


# Views requirements .........
from ..forms import *
from ..models import *
from .road_views import *

# Import optimizer module ............
#from ..optimizer.time_series_forecast import Time_Series_Forecast
#from ..optimizer.intersection_optimizer import *
from ..simulation.generic.generate_network import *

# External libraries .................
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar 
import plotly.express as px

# Testing response ....................................................
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

# Home view .............................................................
def home_(request ):
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    int_id = intersection_list[0].id
    return home(request,1)

def home(request, intersection_id ):
    # Prepare the intersections list --------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 7) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    intersection_form = IntersectionForm()
    road_form = RoadForm()
    # Prepare data for the simulation --------------------------------------
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    roads_in, roads_out = read_road( intersection_id )
    #print( road_list )
    
    # Data passed to the User Interface ------------------------------------
    data_input = {
        #'current_intersection': intersection_id,
        'page_obj': page_obj ,
        'intersection_info': intersection_info,
        'intersection_form': intersection_form ,
        'road_list_in': roads_in,
        'road_list_out': roads_out,
        'road_form': road_form ,
    }
    return render(request, 'main_app/view_home.html', data_input )


# Coordinates of the intersection ..................................................................................
# def visualize_intersection(request, intersection_id):
def visualize_intersection(request):

    # get intersection info
    # intersection = get_list_or_404( Intersection , pk=intersection_id)

    # create visualization/simulation - SUMO
    intersection_type = ""
    road_information = ""
    traffic_lights = ""
    simulation = GenerateNetwork(type=intersection_type, roads=road_information, lights=traffic_lights)
    #simulation.create_network()

    # Data for UI 
    data_input = {
        "intersection_name": ""
    }

    return render(request, 'main_app/road_simulation.html')

# Simulation information for the intersection .......................................................................
def simulate_intersection(request, intersection_id ):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
    

