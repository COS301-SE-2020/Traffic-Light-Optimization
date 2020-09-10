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
    # Different intersections list --------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 7) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # New Intersection form ----------------------------------------------- 
    intersection_form = IntersectionForm()
    # Update road information --------------------------------------------
    
    road_form = RoadForm()
    # Prepare data for the simulation --------------------------------------
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    roads_in, roads_out = read_road( intersection_id )
    
    roads_in_copy = [ road.road_info() for road in roads_in ]
    roads_out_copy = [ road.road_info() for road in roads_out ]
    #print(roads_in_copy)

    rate = {'rate':100}
    for road in roads_in_copy:
        road.update({'rate':100})
    print(roads_in_copy)
    # Calling the simulator -------------------------------------------
    if intersection_info.id > 19 :
        intersection_type = "tleft"
        in_data = [{'name': 'r89', 'capacity': 23, 'speed': 86, 'position': 'A', 'lanes': 1, 'rate':100},
                    {'name': 'r475', 'capacity': 12, 'speed': 32, 'position': 'B', 'lanes': 1, 'rate':100},
                    {'name': 'jack7865', 'capacity': 65, 'speed': 32, 'position': 'C', 'lanes': 1, 'rate':100}]

        out_data = [{'name': 'r505', 'capacity': 24, 'speed': 30, 'position': 'A', 'lanes': 1},
                    {'name': 'wegeg', 'capacity': 32, 'speed': 7, 'position': 'B', 'lanes': 1},
                    {'name': 'u758', 'capacity': 78, 'speed': 45, 'position': 'C', 'lanes': 1}]
                    
        intersection_type = "cross"
        if intersection_info.intersection_type == "T-Up":
            intersection_type = "tup"
        if intersection_info.intersection_type == "T-Down":
            intersection_type = "tdown"
        if intersection_info.intersection_type == "T-Left":
            intersection_type = "tleft"
        if intersection_info.intersection_type == "T-Right":
            intersection_type = "tright"
        in_data = roads_in_copy
        out_data = roads_out_copy
        
        traffic_lights = []
        simulation = GenerateNetwork( type=intersection_type, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
        simulation.create_network()
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
    intersection_type = "tleft"
    in_data = [{'name': 'r89', 'capacity': 23, 'speed': 86, 'position': 'A', 'lanes': 1, 'rate':100},
                {'name': 'r475', 'capacity': 12, 'speed': 32, 'position': 'B', 'lanes': 1, 'rate':100},
                {'name': 'jack7865', 'capacity': 65, 'speed': 32, 'position': 'C', 'lanes': 1, 'rate':100}]

    out_data = [{'name': 'r505', 'capacity': 24, 'speed': 30, 'position': 'A', 'lanes': 1},
                {'name': 'wegeg', 'capacity': 32, 'speed': 7, 'position': 'B', 'lanes': 1},
                {'name': 'u758', 'capacity': 78, 'speed': 45, 'position': 'C', 'lanes': 1}]
    traffic_lights = []
    simulation = GenerateNetwork( type=intersection_type, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
    simulation.create_network()

    # Data for UI 
    data_input = {
        "intersection_name": ""
    }

    return render(request, 'main_app/road_simulation.html')

# Simulation information for the intersection .......................................................................
def simulate_intersection(request, intersection_id ):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
    

