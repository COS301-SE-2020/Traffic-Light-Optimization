# Django requirements ..............
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator

# External libraries .................
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar 
import plotly.express as px

# Import optimizer module ............
#from ..optimizer.time_series_forecast import Time_Series_Forecast
#from ..optimizer.intersection_optimizer import *

# Views requirements .................
from ..forms import *
from ..models import *

from .road_views import *
from ..simulation.generic.generate_network import *
    
# Create Intersection ..............................................................................................
def create_intersection(request):
    if request.method == 'POST':
        #perform required operations
        form_intersection = IntersectionForm(request.POST)
        if form_intersection.is_valid():
            new_intersection = form_intersection.save()
            new_intersection.network_id = get_object_or_404( Network, pk=1)
            new_intersection.save()

            # Add default roads to this intersection
            dist, spd, lan = 80, 10, 1
            if new_intersection.intersection_type != "T-Up":
                Road.objects.create( 
                    intersection_in=new_intersection, road_name="inA",  position="A", road_distance=dist, average_speed=spd, num_lanes=lan ) 
                Road.objects.create(
                    intersection_out=new_intersection, road_name="outA", position="A", road_distance=dist, average_speed=spd, num_lanes=lan )

            if new_intersection.intersection_type != "T-Right":   
                Road.objects.create( 
                    intersection_in=new_intersection , road_name="inB", position="B", road_distance=dist, average_speed=spd, num_lanes=lan )
                Road.objects.create( 
                    intersection_out=new_intersection , road_name="outB", position="B", road_distance=dist, average_speed=spd, num_lanes=lan )
            
            if new_intersection.intersection_type != "T-Down":
                Road.objects.create( 
                    intersection_in=new_intersection, road_name="inC", position="C", road_distance=dist, average_speed=spd, num_lanes=lan )
                Road.objects.create( 
                    intersection_out=new_intersection, road_name="outC", position="C", road_distance=dist, average_speed=spd, num_lanes=lan )

            if new_intersection.intersection_type != "T-Left":
                Road.objects.create( 
                    intersection_in=new_intersection, road_name="inD", position="D", road_distance=dist, average_speed=spd, num_lanes=lan )
                Road.objects.create( 
                    intersection_out=new_intersection, road_name="outD", position="D", road_distance=dist, average_speed=spd, num_lanes=lan )

            # Create the simulation files from default settings
            in_ , out_ = read_road( new_intersection.id )
            in_data = [ r.road_info() for r in in_ ]
            out_data = [ r.road_info() for r in out_ ]
            for road in in_data:
                road.update({'rate':100})
            traffic_lights = []
            inter_object = get_object_or_404( Intersection, pk=new_intersection.id)
            print( inter_object.id )
            print( "......................" )
            simulation = GenerateNetwork( intersection_obj=inter_object, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
            #simulation.create_network()
            simulation.create_simulation_configurations()
            return HttpResponseRedirect(reverse('home', args=(new_intersection.id, ))) 
    return HttpResponseRedirect(reverse('home_'))


# Update OR Delete Intersection ...............................................................................................
def update_delete_intersection(request, intersection_id):
    intersection = get_object_or_404( Intersection, pk=intersection_id)
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home', args=(intersection.id, ))) 
    
    intersection.delete()
    return HttpResponseRedirect(reverse('home_')) 


# Upload historic Data for forecasting future traffic ..............................................................
def upload_historic_data(request, intersection_id ):

    if request.method == 'POST':
        data_file = request.FILES['historic_data']
        # Open data in pandas 
        df = pd.read_csv(data_file, header=None)
        headers = df[0]

        # Get roads to validate data 
        roads = read_road( intersection_id )
        roads_in = roads.roads_in
        # Validate headers
        if len(roads_in) > 1 :
            csv_road_names = headers[1:]
            count = 0
            for road in roads_in:
                if road.road_name in csv_road_names:
                    count = count + 1
            if( len(roads_in) == count ):
                intersection = get_object_or_404( Intersection, pk=intersection_id)
                intersection.upload_historic_data( data_file )
                intersection.train_model()
                intersection.forecast_traffic()
                intersection.optimize_traffic_lights()
        # Error 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 
   
# Forecast the uploaded data .......................................................................................
def forecast_intersection( date):
    tsf_services = Time_Series_Forecast()
    data = tsf_services.prepare_data()
    tsf_services.forecast_model()
    results = tsf_services.prediction()
    return data , results


# Calculate the time for each day ...................................................................................
def optimize_intersection( request , intersection_id):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))

def update_simulation_info( request , intersection_id):
    # get intersection
    intersection = get_object_or_404( Intersection, pk=intersection_id)

    # Create the simulation files from updated Road settings
    in_data, out_data = read_road( intersection.id )
    in_data = [ r.road_info() for r in in_data ]
    out_data = [ r.road_info() for r in out_data ]
    for road in in_data:
        road.update({'rate':100})
    traffic_lights = []
    simulation = GenerateNetwork( intersection_obj=intersection, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
    #simulation.create_network()
    simulation.create_simulation_configurations()

    return HttpResponseRedirect(reverse('home', args=( intersection_id, ))) 



    