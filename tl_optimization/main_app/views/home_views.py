# Headers ................
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from threading import Thread

# Views requirements .........
from ..forms import *
from ..models import *
from .road_views import *

# Simulation module
from ..simulation.generic import *
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

# Global Variable ..........................
GLOBAL_stop_threads = True

# Testing response ....................................................
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

# Home view .............................................................
def home_(request ):
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    intersection = intersection_list[0]
    int_id = intersection.id
    return home(request,int_id)

def home(request, intersection_id ):
    # Different intersections list --------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 7) # Show 7 intersections per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # New Intersection form ----------------------------------------------- 
    intersection_form = IntersectionForm()

    # Prepare data for the simulation --------------------------------------
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    roads_in, roads_out = read_road( intersection_id )
    Simulation = Thread(target=initiate,args=(intersection_id,) )
    Simulation.start() 

    # Update road information --------------------------------------------
    rforms_in = [ RoadForm(instance=get_object_or_404( Road, pk=r.road_info().get("id"))) for r in roads_in]
    rforms_out = [ RoadForm(instance=get_object_or_404( Road, pk=r.road_info().get("id"))) for r in roads_out]
    count = [ v for v in range(len(rforms_out))]
    road_forms = zip(rforms_in,rforms_out,count)
    road_form = RoadForm()

    # Calling the simulator -------------------------------------------

    # Data passed to the User Interface ------------------------------------
    data_input = {
        #'current_intersection': intersection_id,
        'page_obj': page_obj ,
        'intersection_info': intersection_info,
        'intersection_form': intersection_form ,
        'road_list_in': roads_in,
        'road_list_out': roads_out,
        'road_form': road_form ,
        'road_forms': road_forms,
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
    

